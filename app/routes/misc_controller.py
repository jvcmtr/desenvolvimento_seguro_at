from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

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