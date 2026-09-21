from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from app.database.database import get_session
from app.models.core.Users import User

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/", response_model=List[User])
def listar_usuarios(session: Session = Depends(get_session)):
    statement = select(User)
    return session.exec(statement).all()

@router.get("/{user_id}", response_model=User)
def buscar_usuario(user_id: int, session: Session = Depends(get_session)):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado")
    return user

@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
def criar_usuario(user: User, session: Session = Depends(get_session)):
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

@router.put("/{user_id}", response_model=User)
def atualizar_usuario(user_id: int, user_data: User, session: Session = Depends(get_session)):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado")
    
    data_dict = user_data.model_dump(exclude_unset=True)
    for key, value in data_dict.items():
        setattr(user, key, value)

    session.add(user)
    session.commit()
    session.refresh(user)
    return user

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_usuario(user_id: int, session: Session = Depends(get_session)):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado")
    session.delete(user)
    session.commit()
    return None