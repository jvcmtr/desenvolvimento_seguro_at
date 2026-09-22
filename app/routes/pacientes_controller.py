from app.config import settings
from datetime import datetime, timezone
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from app.database.database import get_session
from app.models.consultas.Paciente import Paciente
from app.dtos.paciente_dto import PacientePostModel, PacienteViewModel

router = APIRouter(prefix="/pacientes", tags=["pacientes"])

@router.get("/", response_model=List[PacienteViewModel])
def listar_pacientes(session: Session = Depends(get_session)):
    statement = select(Paciente)
    return [PacienteViewModel.create_from(x) for x in session.exec(statement).all()]


@router.get("/{paciente_id}", response_model=PacienteViewModel)
def buscar_paciente(paciente_id: int, session: Session = Depends(get_session)):
    paciente = session.get(Paciente, paciente_id)
    if not paciente:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Paciente não encontrado")
    return PacienteViewModel.create_from(paciente)


@router.post("/", response_model=Paciente, status_code=status.HTTP_201_CREATED)
def criar_paciente(paciente_dto: PacientePostModel, session: Session = Depends(get_session)):
    paciente = paciente_dto.as_model()
    paciente.created_by = paciente.nome
    paciente.created_by_user_id = settings.SYSTEM_USER_ID

    session.add(paciente)
    session.commit()
    session.refresh(paciente)
    return paciente


@router.put("/{paciente_id}", response_model=Paciente)
def atualizar_paciente(paciente_id: int, paciente_data: PacientePostModel, session: Session = Depends(get_session)):
    paciente = session.get(Paciente, paciente_id)
    if not paciente:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Paciente não encontrado")
    
    paciente_data.update(paciente)

    session.add(paciente)
    session.commit()
    session.refresh(paciente)
    return paciente


@router.delete("/{paciente_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_paciente(paciente_id: int, session: Session = Depends(get_session)):
    paciente = session.get(Paciente, paciente_id)
    if not paciente:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Paciente não encontrado")
    
    # soft delete
    paciente.deleted_at = datetime.now(timezone.utc)
    paciente.deleted_by_user_id = settings.SYSTEM_USER_ID
    paciente.deleted_by = "SYSTEM"

    session.commit()
    return None