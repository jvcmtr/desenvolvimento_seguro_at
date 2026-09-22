from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from app.database.database import get_session
from app.models.core.Users import User
from .dtos.user_dto import UserPostModel, UserViewModel

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/", response_model=List[UserViewModel])
def listar_usuarios(session: Session = Depends(get_session)):
    statement = select(User)
    return [ UserViewModel.create_from(x) for x in session.exec(statement).all() ]


@router.get("/{user_id}", response_model=UserViewModel)
def buscar_usuario(user_id: int, session: Session = Depends(get_session)):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado")
    return UserViewModel.create_from(user)


@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
def criar_usuario(user_dt: UserPostModel, session: Session = Depends(get_session)):
    user = user_dt.as_model()
    user.created_by = user.username

    session.add(user)
    session.commit()
    session.refresh(user)
    return user



@router.put("/{user_id}", response_model=User)
def atualizar_usuario(user_id: int, user_data: UserPostModel, session: Session = Depends(get_session)):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado")
    
    user_data.update(user)

    session.add(user)
    session.commit()
    session.refresh(user)
    return user



@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_usuario(user_id: int, session: Session = Depends(get_session)):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado")
    
    #soft delete
    user.deleted_at = datetime.date()
    user.deleted_by_user_id = settings.SYSTEM_USER_ID
    user.deleted_by = "SYSTEM"
    
    session.commit()
    return None