from datetime import datetime, timezone
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from app.config import settings
from app.database.database import get_session
from app.models.consultas.Consulta import Consulta
from app.routes.dtos.consulta_dto import ConsultaPostModel, ConsultaViewModel


from app.models.core.Users import User
from app.core.auth import get_current_user, verify_entity_ownership

router = APIRouter(prefix="/consultas", tags=["consultas"])

@router.get("/", response_model=List[ConsultaViewModel])
def listar_consultas(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):

    statement = select(Consulta).where(Consulta.deleted_at.is_(None))
    consultas = session.exec(statement).all()
    
    temp = []
    for c in consultas:
        try:
            verify_entity_ownership(c, current_user)
            temp.append(c)
        except Exception:
            continue

    return [ConsultaViewModel.create_from(x) for x in temp]


@router.get("/{consulta_id}", response_model=ConsultaViewModel)
def buscar_consulta(
    consulta_id: int, 
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    consulta = session.get(Consulta, consulta_id)
    if not consulta or consulta.is_deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Consulta não encontrada")
    
    verify_entity_ownership(consulta, current_user)
    return ConsultaViewModel.create_from(consulta)


@router.post("/", response_model=Consulta, status_code=status.HTTP_201_CREATED)
def criar_consulta(
    consulta_dto: ConsultaPostModel, 
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    consulta = consulta_dto.as_model()
    consulta.created_at = datetime.now(timezone.utc)
    consulta.created_by = current_user.username
    consulta.created_by_user_id = current_user.id

    session.add(consulta)
    session.commit()
    session.refresh(consulta)
    return consulta


@router.put("/{consulta_id}", response_model=Consulta)
def atualizar_consulta(
    consulta_id: int, 
    consulta_data: ConsultaPostModel, 
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    consulta = session.get(Consulta, consulta_id)
    if not consulta or consulta.is_deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Consulta não encontrada")
    
    verify_entity_ownership(consulta, current_user)

    consulta_data.update(consulta)
    consulta.updated_at = datetime.now(timezone.utc)
    consulta.updated_by_user_id = current_user.id
    consulta.updated_by = current_user.username

    session.add(consulta)
    session.commit()
    session.refresh(consulta)
    return consulta


@router.delete("/{consulta_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_consulta(
    consulta_id: int, 
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    consulta = session.get(Consulta, consulta_id)
    if not consulta or consulta.is_deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Consulta não encontrada")
    
    verify_entity_ownership(consulta, current_user)

    # soft delete
    consulta.deleted_at = datetime.now(timezone.utc)
    consulta.deleted_by_user_id = current_user.id
    consulta.deleted_by = current_user.username

    session.commit()
    return None