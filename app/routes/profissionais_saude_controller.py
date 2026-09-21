from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from app.database.database import get_session
from app.models.consultas.ProfissionalSaude import ProfissionalSaude

router = APIRouter(prefix="/profissionais", tags=["profissionais de saude"])

@router.get("/", response_model=List[ProfissionalSaude])
def listar_profissionais(session: Session = Depends(get_session)):
    statement = select(ProfissionalSaude)
    return session.exec(statement).all()

@router.get("/{profissional_id}", response_model=ProfissionalSaude)
def buscar_profissional(profissional_id: int, session: Session = Depends(get_session)):
    profissional = session.get(ProfissionalSaude, profissional_id)
    if not profissional:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profissional de saúde não encontrado")
    return profissional

@router.post("/", response_model=ProfissionalSaude, status_code=status.HTTP_201_CREATED)
def criar_profissional(profissional: ProfissionalSaude, session: Session = Depends(get_session)):
    session.add(profissional)
    session.commit()
    session.refresh(profissional)
    return profissional

@router.put("/{profissional_id}", response_model=ProfissionalSaude)
def atualizar_profissional(profissional_id: int, profissional_data: ProfissionalSaude, session: Session = Depends(get_session)):
    profissional = session.get(ProfissionalSaude, profissional_id)
    if not profissional:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profissional de saúde não encontrado")
    
    data_dict = profissional_data.model_dump(exclude_unset=True)
    for key, value in data_dict.items():
        setattr(profissional, key, value)

    session.add(profissional)
    session.commit()
    session.refresh(profissional)
    return profissional

@router.delete("/{profissional_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_profissional(profissional_id: int, session: Session = Depends(get_session)):
    profissional = session.get(ProfissionalSaude, profissional_id)
    if not profissional:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profissional de saúde não encontrado")
    session.delete(profissional)
    session.commit()
    return None