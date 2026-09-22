from datetime import datetime
from pydantic import BaseModel
from app.models.consultas.Paciente import Paciente

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
    id: int | None = None
    nome: str
    cpf: str
    dt_nasc: datetime
    email: str
    telefone: str

    def as_model(self) -> Paciente:
        return Paciente(**self.__dict__)

    def update(self, paciente: Paciente) -> Paciente:
        paciente.nome = self.nome
        paciente.cpf = self.cpf
        paciente.dt_nasc = self.dt_nasc
        paciente.email = self.email
        paciente.telefone = self.telefone

        paciente.updated_at = datetime.now()
        
        return paciente