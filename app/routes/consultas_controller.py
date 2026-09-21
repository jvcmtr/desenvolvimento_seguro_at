from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from app.database.database import get_session
from app.models.consultas.Consulta import Consulta

router = APIRouter(prefix="/consultas", tags=["consultas"])

@router.get("/", response_model=List[Consulta])
def listar_consultas(session: Session = Depends(get_session)):
    statement = select(Consulta)
    return session.exec(statement).all()

@router.get("/{consulta_id}", response_model=Consulta)
def buscar_consulta(consulta_id: int, session: Session = Depends(get_session)):
    consulta = session.get(Consulta, consulta_id)
    if not consulta:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Consulta não encontrada")
    return consulta

@router.post("/", response_model=Consulta, status_code=status.HTTP_201_CREATED)
def criar_consulta(consulta: Consulta, session: Session = Depends(get_session)):
    session.add(consulta)
    session.commit()
    session.refresh(consulta)
    return consulta

@router.put("/{consulta_id}", response_model=Consulta)
def atualizar_consulta(consulta_id: int, consulta_data: Consulta, session: Session = Depends(get_session)):
    consulta = session.get(Consulta, consulta_id)
    if not consulta:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Consulta não encontrada")
    
    data_dict = consulta_data.model_dump(exclude_unset=True)
    for key, value in data_dict.items():
        setattr(consulta, key, value)

    session.add(consulta)
    session.commit()
    session.refresh(consulta)
    return consulta

@router.delete("/{consulta_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_consulta(consulta_id: int, session: Session = Depends(get_session)):
    consulta = session.get(Consulta, consulta_id)
    if not consulta:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Consulta não encontrada")
    session.delete(consulta)
    session.commit()
    return None