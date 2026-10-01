from datetime import datetime, timezone
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from app.config import settings
from app.database.database import get_session
from app.models.consultas.ProfissionalSaude import ProfissionalSaude
from app.routes.dtos.profissional_saude_dto import ProfissionalSaudePostModel, ProfissionalSaudeViewModel

from app.models.core.Users import User
from app.core.auth import get_current_user, verify_entity_ownership, select_owned_entities

router = APIRouter(prefix="/profissionais", tags=["profissionais de saude"])


@router.get("/", response_model=List[ProfissionalSaudeViewModel])
def listar_profissionais(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    statement = select_owned_entities(ProfissionalSaude, current_user).where(ProfissionalSaude.deleted_at.is_(None))
    profissionais = session.exec(statement).all()
    
    return [ProfissionalSaudeViewModel.create_from(x) for x in profissionais]


@router.get("/{profissional_id}", response_model=ProfissionalSaudeViewModel)
def buscar_profissional(
    profissional_id: int, 
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    profissional = session.get(ProfissionalSaude, profissional_id)
    if not profissional or profissional.is_deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profissional de saúde não encontrado")
    
    verify_entity_ownership(profissional, current_user)
    return ProfissionalSaudeViewModel.create_from(profissional)


@router.post("/", response_model=ProfissionalSaude, status_code=status.HTTP_201_CREATED)
def criar_profissional(
    profissional_dto: ProfissionalSaudePostModel, 
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    profissional = profissional_dto.as_model()
    profissional.created_at = datetime.now(timezone.utc)
    profissional.created_by = current_user.username
    profissional.created_by_user_id = current_user.id

    session.add(profissional)
    session.commit()
    session.refresh(profissional)

    return ProfissionalSaudeViewModel.create_from(profissional)


@router.put("/{profissional_id}", response_model=ProfissionalSaude)
def atualizar_profissional(
    profissional_id: int, 
    profissional_data: ProfissionalSaudePostModel, 
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    profissional = session.get(ProfissionalSaude, profissional_id)
    if not profissional or profissional.is_deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profissional de saúde não encontrado")
    
    verify_entity_ownership(profissional, current_user)

    profissional_data.update(profissional)
    profissional.updated_at = datetime.now(timezone.utc)
    profissional.updated_by_user_id = current_user.id
    profissional.updated_by = current_user.username

    session.add(profissional)
    session.commit()
    session.refresh(profissional)

    return ProfissionalSaudeViewModel.create_from(profissional)



@router.delete("/{profissional_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_profissional(
    profissional_id: int, 
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    profissional = session.get(ProfissionalSaude, profissional_id)
    if not profissional or profissional.is_deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profissional de saúde não encontrado")
    
    verify_entity_ownership(profissional, current_user)

    # soft delete
    profissional.deleted_at = datetime.now(timezone.utc)
    profissional.deleted_by_user_id = current_user.id
    profissional.deleted_by = current_user.username

    session.commit()

    return None