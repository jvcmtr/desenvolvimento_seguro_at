from datetime import datetime
from pydantic import BaseModel, Field
from app.models.consultas.Paciente import Paciente
from app.models.core.Users import User

class PacienteViewModel(BaseModel):
    id: int
    nome: str
    cpf: str
    dt_nasc: datetime
    email: str
    telefone: str
    created_at: datetime

    @classmethod
    def create_from(cls, paciente: Paciente) -> "PacienteViewModel":
        return cls(**paciente.__dict__)


class PacientePostModel(BaseModel):
    model_config = ConfigDict(extra="forbid")
    
    id: int | None = None
    nome: str = Field(..., max_length=100)
    cpf : str = Field(..., pattern=r"^\d{3}\.\d{3}\.\d{3}-\d{2}$|^\d{11}$")
    email   : str = Field(..., pattern= r"^[\w.-]+@[\w.-]+\.[A-Za-z]{2,4}$")
    telefone: str = Field(..., pattern=r"^\+?[\d\s\-\(\)]{8,20}$")
    dt_nasc: datetime

    def as_model(self) -> Paciente:
        return Paciente(**self.__dict__)

    def update(self, paciente: Paciente) -> Paciente:
        paciente.nome = self.nome
        paciente.cpf = self.cpf
        paciente.dt_nasc = self.dt_nasc
        paciente.email = self.email
        paciente.telefone = self.telefone
        
        return paciente