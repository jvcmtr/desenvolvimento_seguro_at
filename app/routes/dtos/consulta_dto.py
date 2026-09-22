from datetime import datetime
from pydantic import BaseModel
from app.models.consultas.Consulta import Consulta, StatusConsulta
import paciente_dto.PacienteViewModel, profissional_saude_dto.ProfissionalSaudeViewModel

class ConsultaViewModel(BaseModel):
    id: int
    paciente_id: int
    paciente: PacienteViewModel

    profissional_id: int
    profissional: ProfissionalSaudeViewModel

    data_hora: datetime
    status: StatusConsulta
    created_at: datetime

    @classmethod
    def create_from(cls, consulta: Consulta) -> "ConsultaViewModel":
        return cls(**{
            **consulta.__dict__,
            "paciente": PacienteViewModel.create_from(consulta.paciente) if consulta.paciente_id else None,
            "profissional": ProfissionalSaudeViewModel.create_from(consulta.profissional_id) if consulta.profissional_id else None,
        })


class ConsultaPostModel(BaseModel):
    id: int | None = None
    paciente_id: int
    profissional_id: int
    data_hora: datetime
    status: StatusConsulta = StatusConsulta.AGENDADA

    def as_model(self) -> Consulta:
        return Consulta(**self.__dict__)

    def update(self, consulta: Consulta) -> Consulta:
        consulta.paciente_id = self.paciente_id
        consulta.profissional_id = self.profissional_id
        consulta.data_hora = self.data_hora
        consulta.status = self.status

        consulta.updated_at = datetime.now()
        
        return consulta