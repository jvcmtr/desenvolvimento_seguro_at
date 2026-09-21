from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.config import settings
from app.routes.misc_controller import router as MISC_ROUTER
from app.routes.users_controller import router as USERS_ROUTER
from app.routes.pacientes_controller import router as PACIENTES_ROUTER
from app.routes.profissionais_saude_controller import router as PROFISSIONAIS_ROUTER
from app.routes.consultas_controller import router as CONSULTAS_ROUTER
from app.tools.setup_db import setup_db

# CONFIG DB
@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_db()
    yield


app = FastAPI(lifespan=lifespan)

# STATIC FILES
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/documents", StaticFiles(directory="docs"), name="documents")
# app.mount("/sourcecode", StaticFiles(directory="app"), name="app") # Extremamente inseguro pois permite verificar __pycache__

# ROUTERS
app.include_router(MISC_ROUTER)
app.include_router(USERS_ROUTER)
app.include_router(PACIENTES_ROUTER)
app.include_router(PROFISSIONAIS_ROUTER)
app.include_router(CONSULTAS_ROUTER)


# MANUAL TESTING
# if settings.IS_DEV:
#     import app.tools.arbitrary_script