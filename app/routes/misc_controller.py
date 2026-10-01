from fastapi import APIRouter, Request, Depends, HTTPException, status
from fastapi.templating import Jinja2Templates

from app.models.core.Users import User, UserRole
from app.core.auth import get_current_user, verify_entity_ownership

router = APIRouter(tags=["misc"])
templates = Jinja2Templates(directory="app/views")

@router.get("/ping")
def get():
    return "App ativo"


@router.get("/")
async def home(request: Request):
    return templates.TemplateResponse(
        request= request,
        name="home_page.html"
    )

@router.get("/adm-ping")
async def home(current_user: User = Depends(get_current_user)):
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code= status.HTTP_403_FORBIDDEN,
            detail="Somente usuarios admin podem acessar esta rota."
        )
    return "Você é ADMIN"