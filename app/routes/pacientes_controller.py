from app.config import settings
from datetime import datetime, timezone
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from app.database.database import get_session
from app.models.consultas.Paciente import Paciente
from app.routes.dtos.paciente_dto import PacientePostModel, PacienteViewModel

from app.models.core.Users import User
from app.core.auth import get_current_user, verify_entity_ownership

router = APIRouter(prefix="/pacientes", tags=["pacientes"])

@router.get("/", response_model=List[PacienteViewModel])
def listar_pacientes(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
    ):

    statement = select(Paciente).where(Paciente.deleted_at.is_(None))
    pacientes = session.exec(statement).all()
    
    temp = []
    for p in pacientes:
        try:
            verify_entity_ownership(p, current_user)
            temp.append(p)
        except:
            continue

    return [PacienteViewModel.create_from(x) for x in temp]


@router.get("/{paciente_id}", response_model=PacienteViewModel)
def buscar_paciente(
    paciente_id: int, 
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
    ):

    paciente = session.get(Paciente, paciente_id)
    if not paciente or paciente.is_deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Paciente não encontrado")

    verify_entity_ownership(paciente, current_user)
    
    return PacienteViewModel.create_from(paciente)


@router.post("/", response_model=Paciente, status_code=status.HTTP_201_CREATED)
def criar_paciente(
    paciente_dto: PacientePostModel, 
    session: Session = Depends(get_session), 
    current_user: User = Depends(get_current_user)
    ):
    
    paciente = paciente_dto.as_model()
    paciente.created_at = datetime.now(timezone.utc)
    paciente.created_by = current_user.username
    paciente.created_by_user_id = current_user.id

    session.add(paciente)
    session.commit()
    session.refresh(paciente)
    return paciente


@router.put("/{paciente_id}", response_model=Paciente)
def atualizar_paciente(
    paciente_id: int, 
    paciente_data: PacientePostModel, 
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
    ):
    paciente = session.get(Paciente, paciente_id)

    if not paciente or paciente.is_deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Paciente não encontrado")
    
    verify_entity_ownership(paciente, current_user)
    
    paciente_data.update(paciente)
    paciente.updated_at_at = datetime.now(timezone.utc)
    paciente.updated_by_user_id = current_user.id
    paciente.updated_by = current_user.username

    session.add(paciente)
    session.commit()
    session.refresh(paciente)
    return paciente


@router.delete("/{paciente_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_paciente(
    paciente_id: int, 
    session: Session = Depends(get_session), 
    current_user: User = Depends(get_current_user)
    ):
    
    paciente = session.get(Paciente, paciente_id)
    if not paciente or paciente.is_deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Paciente não encontrado")
    
    verify_entity_ownership(paciente, current_user)
    # soft delete
    paciente.deleted_at = datetime.now(timezone.utc)
    paciente.deleted_by_user_id = current_user.id
    paciente.deleted_by = current_user.username

    session.commit()
    return None