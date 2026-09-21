from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from app.database.database import get_session
from app.models.consultas.Paciente import Paciente

router = APIRouter(prefix="/pacientes", tags=["pacientes"])

@router.get("/", response_model=List[Paciente])
def listar_pacientes(session: Session = Depends(get_session)):
    statement = select(Paciente)
    return session.exec(statement).all()

@router.get("/{paciente_id}", response_model=Paciente)
def buscar_paciente(paciente_id: int, session: Session = Depends(get_session)):
    paciente = session.get(Paciente, paciente_id)
    if not paciente:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Paciente não encontrado")
    return paciente

@router.post("/", response_model=Paciente, status_code=status.HTTP_201_CREATED)
def criar_paciente(paciente: Paciente, session: Session = Depends(get_session)):
    session.add(paciente)
    session.commit()
    session.refresh(paciente)
    return paciente

@router.put("/{paciente_id}", response_model=Paciente)
def atualizar_paciente(paciente_id: int, paciente_data: Paciente, session: Session = Depends(get_session)):
    paciente = session.get(Paciente, paciente_id)
    if not paciente:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Paciente não encontrado")
    
    data_dict = paciente_data.model_dump(exclude_unset=True)
    for key, value in data_dict.items():
        setattr(paciente, key, value)

    session.add(paciente)
    session.commit()
    session.refresh(paciente)
    return paciente

@router.delete("/{paciente_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_paciente(paciente_id: int, session: Session = Depends(get_session)):
    paciente = session.get(Paciente, paciente_id)
    if not paciente:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Paciente não encontrado")
    session.delete(paciente)
    session.commit()
    return None