from app.config import settings
from datetime import datetime, timezone
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from app.database.database import get_session
from app.models.consultas.Consulta import Consulta
from app.dtos.consulta_dto import ConsultaPostModel, ConsultaViewModel

router = APIRouter(prefix="/consultas", tags=["consultas"])

@router.get("/", response_model=List[ConsultaViewModel])
def listar_consultas(session: Session = Depends(get_session)):
    statement = select(Consulta)
    return [ConsultaViewModel.create_from(x) for x in session.exec(statement).all()]


@router.get("/{consulta_id}", response_model=ConsultaViewModel)
def buscar_consulta(consulta_id: int, session: Session = Depends(get_session)):
    consulta = session.get(Consulta, consulta_id)
    if not consulta:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Consulta não encontrada")
    return ConsultaViewModel.create_from(consulta)


@router.post("/", response_model=Consulta, status_code=status.HTTP_201_CREATED)
def criar_consulta(consulta_dto: ConsultaPostModel, session: Session = Depends(get_session)):
    consulta = consulta_dto.as_model()
    consulta.created_by = "SYSTEM"
    consulta.created_by_user_id = settings.SYSTEM_USER_ID

    session.add(consulta)
    session.commit()
    session.refresh(consulta)
    return consulta


@router.put("/{consulta_id}", response_model=Consulta)
def atualizar_consulta(consulta_id: int, consulta_data: ConsultaPostModel, session: Session = Depends(get_session)):
    consulta = session.get(Consulta, consulta_id)
    if not consulta:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Consulta não encontrada")
    
    consulta_data.update(consulta)

    session.add(consulta)
    session.commit()
    session.refresh(consulta)
    return consulta


@router.delete("/{consulta_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_consulta(consulta_id: int, session: Session = Depends(get_session)):
    consulta = session.get(Consulta, consulta_id)
    if not consulta:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Consulta não encontrada")
    
    # soft delete
    consulta.deleted_at = datetime.now(timezone.utc)
    consulta.deleted_by_user_id = settings.SYSTEM_USER_ID
    consulta.deleted_by = "SYSTEM"

    session.commit()
    return None