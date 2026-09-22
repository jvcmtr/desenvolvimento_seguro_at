from datetime import datetime
from pydantic import BaseModel
from app.models.consultas.ProfissionalSaude import ProfissionalSaude

class ProfissionalSaudeViewModel(BaseModel):
    id: int
    nome: str
    cpf: str
    dt_nasc: datetime
    especialidade: str
    registro_profissional: str
    created_at: datetime

    @classmethod
    def create_from(cls, profissional: ProfissionalSaude) -> "ProfissionalSaudeViewModel":
        return cls(**profissional.__dict__)


class ProfissionalSaudePostModel(BaseModel):
    id: int | None = None
    nome: str
    cpf: str
    dt_nasc: datetime
    especialidade: str
    registro_profissional: str

    def as_model(self) -> ProfissionalSaude:
        return ProfissionalSaude(**self.__dict__)

    def update(self, profissional: ProfissionalSaude) -> ProfissionalSaude:
        profissional.nome = self.nome
        profissional.cpf = self.cpf
        profissional.dt_nasc = self.dt_nasc
        profissional.especialidade = self.especialidade
        profissional.registro_profissional = self.registro_profissional

        profissional.updated_at = datetime.now()
        
        return profissional