from app.config import settings
from datetime import datetime, timezone
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from app.database.database import get_session
from app.models.consultas.ProfissionalSaude import ProfissionalSaude
from app.dtos.profissional_saude_dto import ProfissionalSaudePostModel, ProfissionalSaudeViewModel

router = APIRouter(prefix="/profissionais", tags=["profissionais de saude"])

@router.get("/", response_model=List[ProfissionalSaudeViewModel])
def listar_profissionais(session: Session = Depends(get_session)):
    statement = select(ProfissionalSaude)
    return [ProfissionalSaudeViewModel.create_from(x) for x in session.exec(statement).all()]


@router.get("/{profissional_id}", response_model=ProfissionalSaudeViewModel)
def buscar_profissional(profissional_id: int, session: Session = Depends(get_session)):
    profissional = session.get(ProfissionalSaude, profissional_id)
    if not profissional:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profissional de saúde não encontrado")
    return ProfissionalSaudeViewModel.create_from(profissional)


@router.post("/", response_model=ProfissionalSaude, status_code=status.HTTP_201_CREATED)
def criar_profissional(profissional_dto: ProfissionalSaudePostModel, session: Session = Depends(get_session)):
    profissional = profissional_dto.as_model()
    profissional.created_by = profissional.nome
    profissional.created_by_user_id = settings.SYSTEM_USER_ID

    session.add(profissional)
    session.commit()
    session.refresh(profissional)
    return profissional


@router.put("/{profissional_id}", response_model=ProfissionalSaude)
def atualizar_profissional(profissional_id: int, profissional_data: ProfissionalSaudePostModel, session: Session = Depends(get_session)):
    profissional = session.get(ProfissionalSaude, profissional_id)
    if not profissional:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profissional de saúde não encontrado")
    
    profissional_data.update(profissional)

    session.add(profissional)
    session.commit()
    session.refresh(profissional)
    return profissional


@router.delete("/{profissional_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_profissional(profissional_id: int, session: Session = Depends(get_session)):
    profissional = session.get(ProfissionalSaude, profissional_id)
    if not profissional:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profissional de saúde não encontrado")
    
    # soft delete
    profissional.deleted_at = datetime.now(timezone.utc)
    profissional.deleted_by_user_id = settings.SYSTEM_USER_ID
    profissional.deleted_by = "SYSTEM"

    session.commit()
    return None