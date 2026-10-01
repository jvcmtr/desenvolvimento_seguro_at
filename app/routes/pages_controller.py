from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.templating import Jinja2Templates
from sqlmodel import Session, select

from app.database.database import get_session

from app.models.consultas.Paciente import Paciente
from app.routes.dtos.paciente_dto import PacientePostModel, PacienteViewModel
from app.models.consultas.Consulta import Consulta
from app.routes.dtos.consulta_dto import ConsultaPostModel, ConsultaViewModel
from app.models.consultas.ProfissionalSaude import ProfissionalSaude
from app.routes.dtos.profissional_saude_dto import ProfissionalSaudePostModel, ProfissionalSaudeViewModel

from app.models.core.Users import User
from app.core.auth import get_current_user, verify_entity_ownership

router = APIRouter(prefix="/html", tags=["html views"])
templates = Jinja2Templates(directory="app/views")

# PACIENTES
@router.get("/pacientes")
def listar_pacientes(
    request: Request, 
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    statement = select(Paciente).where(Paciente.deleted_at.is_(None))
    pacientes = session.exec(statement).all()

    temp = []
    for p in pacientes:
        try:
            verify_entity_ownership(p, current_user)
            temp.append(p)
        except Exception:
            continue

    items = [PacienteViewModel.create_from(x).__dict__ for x in temp]
    return templates.TemplateResponse(
        name="default_list_page.html",
        request=request,
        context={"items": items}
    )


@router.get("/pacientes/{paciente_id}")
def buscar_paciente(
    request: Request, 
    paciente_id: int, 
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    paciente = session.get(Paciente, paciente_id)
    if not paciente or getattr(paciente, "is_deleted", False) or paciente.deleted_at is not None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Paciente não encontrado")

    verify_entity_ownership(paciente, current_user)

    return templates.TemplateResponse(
        name="default_details_page.html",
        request=request,
        context={"entity": PacienteViewModel.create_from(paciente).__dict__}
    )



# CONSULTAS
@router.get("/consultas")
def listar_consultas(
    request: Request, 
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    statement = select(Consulta).where(Consulta.deleted_at.is_(None))
    consultas = session.exec(statement).all()

    temp = []
    for c in consultas:
        try:
            verify_entity_ownership(c, current_user)
            temp.append(c)
        except Exception:
            continue

    items = [ConsultaViewModel.create_from(x).__dict__ for x in temp]
    return templates.TemplateResponse(
        name="default_list_page.html",
        request=request,
        context={"items": items}
    )


@router.get("/consultas/{consulta_id}")
def buscar_consulta(
    request: Request, 
    consulta_id: int, 
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    consulta = session.get(Consulta, consulta_id)
    if not consulta or getattr(consulta, "is_deleted", False) or consulta.deleted_at is not None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Consulta não encontrada")

    verify_entity_ownership(consulta, current_user)

    return templates.TemplateResponse(
        name="default_details_page.html",
        request=request,
        context={"entity": ConsultaViewModel.create_from(consulta).__dict__}
    )


# PROFICIONAIS
@router.get("/proficionais_saude/")
def listar_profissionais(
    request: Request, 
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    statement = select(ProfissionalSaude).where(ProfissionalSaude.deleted_at.is_(None))
    profissionais = session.exec(statement).all()

    temp = []
    for p in profissionais:
        try:
            verify_entity_ownership(p, current_user)
            temp.append(p)
        except Exception:
            continue

    items = [ProfissionalSaudeViewModel.create_from(x).__dict__ for x in temp]
    return templates.TemplateResponse(
        name="default_list_page.html",
        request=request,
        context={"items": items}
    )


@router.get("/proficionais_saude/{profissional_id}")
def buscar_profissional(
    request: Request, 
    profissional_id: int, 
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    profissional = session.get(ProfissionalSaude, profissional_id)
    if not profissional or getattr(profissional, "is_deleted", False) or profissional.deleted_at is not None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profissional de saúde não encontrado")

    verify_entity_ownership(profissional, current_user)

    return templates.TemplateResponse(
        name="default_details_page.html",
        request=request,
        context={"entity": ProfissionalSaudeViewModel.create_from(profissional).__dict__}
    )