from datetime import datetime
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlmodel import Session, select
from app.database.database import get_session
from app.models.consultas.Paciente import Paciente
from app.routes.dtos.paciente_dto import PacientePostModel, PacienteViewModel
from app.models.consultas.Consulta import Consulta
from app.routes.dtos.consulta_dto import ConsultaPostModel, ConsultaViewModel
from app.models.consultas.ProfissionalSaude import ProfissionalSaude
from app.routes.dtos.profissional_saude_dto import ProfissionalSaudePostModel, ProfissionalSaudeViewModel
from fastapi.templating import Jinja2Templates

router = APIRouter(prefix="/html", tags=["html views"])
templates = Jinja2Templates(directory="app/views")

# PACIENTES
@router.get("/pacientes")
def listar_pacientes(request: Request, session: Session = Depends(get_session)):
    statement = select(Paciente)
    list = [PacienteViewModel.create_from(x).__dict__ for x in session.exec(statement).all()]
    return templates.TemplateResponse(
        name="default_list_page.html",
        request=request,
        context={"items": list}
    )

@router.get("/pacientes/{paciente_id}")
def buscar_paciente(request: Request, paciente_id: int, session: Session = Depends(get_session)):
    paciente = session.get(Paciente, paciente_id)
    if not paciente:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Paciente não encontrado")
    
    return templates.TemplateResponse(
        name="default_details_page.html",
        request=request,
        context={"entity": PacienteViewModel.create_from(paciente).__dict__ }
    )
    


# CONSULTAS
@router.get("/consultas")
def listar_consultas(request: Request, session: Session = Depends(get_session)):
    statement = select(Consulta)
    list = [ConsultaViewModel.create_from(x).__dict__ for x in session.exec(statement).all()]

    return templates.TemplateResponse(
        name="default_list_page.html",
        request=request,
        context={"items": list}
    )

@router.get("/consultas/{consulta_id}")
def buscar_consulta(request: Request, consulta_id: int, session: Session = Depends(get_session)):
    consulta = session.get(Consulta, consulta_id)
    if not consulta:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Consulta não encontrada")

    return templates.TemplateResponse(
        name="default_details_page.html",
        request=request,
        context={"entity": ConsultaViewModel.create_from(consulta).__dict__}
    )


# PROFICIONAIS
@router.get("/proficionais_saude/")
def listar_profissionais(request: Request, session: Session = Depends(get_session)):
    statement = select(ProfissionalSaude)
    list = [ProfissionalSaudeViewModel.create_from(x).__dict__ for x in session.exec(statement).all()]
    return templates.TemplateResponse(
        name="default_list_page.html",
        request=request,
        context={"items": list}
    )
    
@router.get("/proficionais_saude/{profissional_id}")
def buscar_profissional(request: Request, profissional_id: int, session: Session = Depends(get_session)):
    profissional = session.get(ProfissionalSaude, profissional_id)
    if not profissional:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profissional de saúde não encontrado")

    return templates.TemplateResponse(
        name="default_details_page.html",
        request=request,
        context={"entity": ProfissionalSaudeViewModel.create_from(profissional).__dict__}
    )