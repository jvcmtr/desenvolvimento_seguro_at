from datetime import datetime, timezone
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from app.config import settings
from app.database.database import get_session
from app.models.core.Users import User
from app.routes.dtos.user_dto import UserPostModel, UserViewModel
from app.core.auth import get_current_user, verify_entity_ownership, get_password_hash

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/", response_model=List[UserViewModel])
def listar_usuarios(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    statement = select(User).where(User.deleted_at.is_(None))
    usuarios = session.exec(statement).all()
    
    temp = []
    for u in usuarios:
        try:
            verify_entity_ownership(u, current_user)
            temp.append(u)
        except Exception:
            continue

    return [UserViewModel.create_from(x) for x in temp]


@router.get("/{user_id}", response_model=UserViewModel)
def buscar_usuario(
    user_id: int, 
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    user = session.get(User, user_id)
    
    if not user or user.is_deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado")
    
    verify_entity_ownership(user, current_user)
    return UserViewModel.create_from(user)


@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
def criar_usuario(
    user_dto: UserPostModel, 
    session: Session = Depends(get_session)
):

    if user_dto.role == UserRole.ADMIN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN , detail="Não é possivel elevar os privilegios do usuario")

    user = user_dto.as_model()
    user.password = get_password_hash(user.password) # Hash de senha
    user.created_at = datetime.now(timezone.utc)
    user.created_by = user_dto.username
    user.created_by_user_id = settings.SYSTEM_USER_ID # Valor temporario

    session.add(user)
    session.commit()
    session.refresh(user)
    user.created_by_user_id = user.id # Usuario sempre é criado por ele mesmo
    session.commit()
    return user


@router.put("/{user_id}", response_model=User)
def atualizar_usuario(
    user_id: int, 
    user_data: UserPostModel, 
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    user = session.get(User, user_id)
    if not user or user.is_deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado")
    
    if user_data.role == UserRole.ADMIN and current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN , detail="Não é possivel elevar os privilegios do usuario")

    verify_entity_ownership(user, current_user)

    if user.password != user_data.password:
        user_data.password = get_password_hash(user_data.password)

    user_data.update(user)
    user.updated_at = datetime.now(timezone.utc)
    user.updated_by_user_id = current_user.id
    user.updated_by = current_user.username


    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_usuario(
    user_id: int, 
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    user = session.get(User, user_id)
    if not user or user.is_deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado")
    
    verify_entity_ownership(user, current_user)

    # soft delete
    user.deleted_at = datetime.now(timezone.utc)
    user.deleted_by_user_id = current_user.id
    user.deleted_by = current_user.username
    
    session.commit()
    return None