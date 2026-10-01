from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlmodel import Session, select

from app.database.database import get_session
from app.models.core.Users import User
from app.core.auth import MFA_STORE, create_access_token, register_mfa, verify_password, confirm_mfa_info
from .dtos.core.credentials import MFARequestModel, MFAResponseModel, UserLoginCredentials


router = APIRouter(prefix="/auth", tags=["Autenticação"])


@router.post("/login")
def login( credentials : UserLoginCredentials, session: Session = Depends(get_session)) -> MFAResponseModel: 
    statement = select(User).where(User.username == credentials.username)
    user = session.exec(statement).first()

    if not user or not verify_password(credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Nome de usuário ou senha incorretos."
        )

    access_token = create_access_token(data={"sub": user.username, "user_id": user.id})    
    mfa_code, expires_at = register_mfa(
        token=access_token,
        username=user.username,
        user_id=user.id
    )

    return MFAResponseModel(
        access_token = access_token,
        mfa_code = mfa_code,        # Simula a exibição/envio do código ao dispositivo
        mfa_expires_at = expires_at
    )


@router.post("/confirm-mfa")
def confirm_mfa(data: MFARequestModel):
    found_token = confirm_mfa_info(data.username, data.code)

    return {"message": "MFA confirmado com sucesso! Acesso aos endpoints liberado."}