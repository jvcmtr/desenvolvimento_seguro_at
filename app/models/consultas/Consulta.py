from datetime import datetime
from enum import Enum
from sqlmodel import Field
from app.models.core.AuditResource import AuditResource

# Import para evitar conflito de tabela inxistente ao criar o banco
from app.models.consultas.Paciente import Paciente
from app.models.consultas.ProfissionalSaude import ProfissionalSaude

class StatusConsulta(str, Enum):
    AGENDADA = "AGENDADA"
    REALIZADA = "REALIZADA"
    CANCELADA = "CANCELADA"

class Consulta(AuditResource, table=True):
    paciente_id: int = Field(foreign_key="paciente.id")
    profissional_id: int = Field(foreign_key="profissionalsaude.id")
    data_hora: datetime
    status: StatusConsulta = StatusConsulta.AGENDADA