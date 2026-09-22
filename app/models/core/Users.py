from enum import Enum
from sqlmodel import Field
from app.config import settings
from app.models.core.AuditResource import AuditResource

class UserRole(str, Enum):
    NENHUM = "NENHUM"
    ATENDENTE = "ATENDENTE"
    PROFISSIONAL_DE_SAUDE = "PROFISSIONAL_DE_SAUDE"
    ADMIN = "ADMIN"

class User(AuditResource, table=True):
    username: str = Field(unique=True, index=True)
    password: str
    role: UserRole = UserRole.NENHUM
    
    # Override faz com que todos os usuarios sejam criados pelo sistema
    created_by_user_id: int = settings.SYSTEM_USER_ID
