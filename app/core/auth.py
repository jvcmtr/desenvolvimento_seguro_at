import random
import jwt
from datetime import datetime, timedelta, timezone
from typing import Dict, Optional, Any
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from passlib.context import CryptContext
from sqlmodel import Session, select

from app.config import settings
from app.database.database import get_session
from app.models.core.Users import User, UserRole
from app.models.core.AuditResource import AuditResource
from app.models.core.MFAMetadata import MFAMetadata


JWT_ENCODE_KEY = settings.JWT_ENCODE_KEY
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60*12 # 12h

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = HTTPBearer()

MFA_STORE: Dict[int, MFAMetadata] = {} # {user_id : MFAMetadata}


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_access_token(data: dict) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.USER_JWT_EXPIRES_IN_MINUTES)
    dt = { **data.copy(), "exp": expire }
    return jwt.encode(dt, JWT_ENCODE_KEY, algorithm=ALGORITHM)


def generate_mfa_code() -> str:
    return f"{random.randint(0, 9999):04d}"


def register_mfa(token: str, username: str, user_id: int) -> tuple[str, datetime]:
    mfa_code = generate_mfa_code()
    expires_at = datetime.now(timezone.utc) + timedelta(minutes=settings.MFA_EXPIRE_MINUTES)
    
    MFA_STORE[user_id] = MFAMetadata(
        dispositivo=username, # AQUI username é utilizado no lugar das informações do dispositivo
        user_id=user_id,
        code=mfa_code,
        expires_at=expires_at,
        confirmed=False
    )
    return mfa_code, expires_at


def confirm_mfa_info(username:str, code:str ) -> Optional[MFAMetadata]:
    now = datetime.now(timezone.utc)

    for user_id, mfa_metadata in MFA_STORE.items():
        if mfa_metadata.dispositivo != username: continue
        if mfa_metadata.code != code: continue

        if now >= mfa_metadata.expires_at: 
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Código MFA expirado. Por favor, realize o login novamente."
            )
        
        MFA_STORE[user_id].confirmed = True
        return user_id

    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Informações do MFA invalidas"
    )


async def get_current_user(auth: HTTPAuthorizationCredentials = Depends(oauth2_scheme), session: Session = Depends(get_session) ) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciais invalidas",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(auth.credentials, JWT_ENCODE_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except Exception as e:
        raise credentials_exception

    user = session.exec(
        select(User).where(User.username == username)
    ).first()
    
    if user is None:
        raise credentials_exception

    mfa_session = MFA_STORE.get(user.id)
    
    if not mfa_session or not mfa_session.confirmed:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Insira o código MFA recebido no endpoint '/auth/confirm-mfa'"
        )

    return user


def verify_entity_ownership(resource: AuditResource, current_user: User) -> None:
    if current_user.role == UserRole.ADMIN:
        return
    
    # Somente o criador do recurso ou admin tem a permição de acessar um recurso.
    # Esta logica pode ser melhorada.
    if resource.created_by_user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso negado"
        )

def get_lab_client(auth: HTTPAuthorizationCredentials = Depends(oauth2_scheme)) -> str:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciais M2M inválidas",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(auth.credentials, JWT_ENCODE_KEY, algorithms=[ALGORITHM])
        
        # Garantia técnica exigida pelo jurídico (Claims e Escopos)
        if not payload.get("m2m"):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, 
                detail="Acesso restrito a integrações M2M"
            )
            
        if settings.LAB_REQUIRED_SCOPE not in payload.get("scopes", []):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, 
                detail="O cliente não possui o escopo necessário para esta operação"
            )
            
        return payload.get("sub")
    except Exception:
        raise credentials_exception