from datetime import datetime
from sqlmodel import Field
from app.models.core.AuditResource import AuditResource

class ProfissionalSaude(AuditResource, table=True):
    nome: str
    cpf: str = Field(unique=True, index=True)
    dt_nasc: datetime
    especialidade: str
    registro_profissional: str = Field(unique=True)