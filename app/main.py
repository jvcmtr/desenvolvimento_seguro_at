from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles

from app.config import settings
from app.core.log_config import logger
from app.core.auth import decode_jwt, oauth2_scheme
from app.routes.auth_controller import router as AUTH_ROUTER
from app.routes.users_controller import router as USERS_ROUTER
from app.routes.pacientes_controller import router as PACIENTES_ROUTER
from app.routes.profissionais_saude_controller import router as PROFISSIONAIS_ROUTER
from app.routes.consultas_controller import router as CONSULTAS_ROUTER
from app.routes.pages_controller import router as HTML_ROUTER
from app.routes.misc_controller import router as MISC_ROUTER
from app.tools.setup_db import setup_db

# CONFIG DB
@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_db()
    yield


app = FastAPI(lifespan=lifespan)


# MIDDLEWARES
@app.middleware("http")
async def log_requests(request: Request, call_next):
    
    response = await call_next(request)
    sub = "anonymous user"
    credentials = "NULL"
    try:
        credentials = await oauth2_scheme(request)
        data = decode_jwt(credentials.credentials)
        sub = data.get("sub", "anonymous user")
        sub += f" (id={data.get("user_id", "LAB_CLIENT")})"
    except:
        pass

    logger.info(f"Method: {request.method} | Path: {request.url.path} | Status: {response.status_code} | User: {sub} | Credentials: {credentials}")
    return response


# STATIC FILES
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/documents", StaticFiles(directory="docs"), name="documents")
# app.mount("/sourcecode", StaticFiles(directory="app"), name="app") # Extremamente inseguro pois permite verificar __pycache__

# ROUTERS
app.include_router(AUTH_ROUTER)
app.include_router(USERS_ROUTER)
app.include_router(PACIENTES_ROUTER)
app.include_router(PROFISSIONAIS_ROUTER)
app.include_router(CONSULTAS_ROUTER)
app.include_router(HTML_ROUTER)
app.include_router(MISC_ROUTER)


# MANUAL TESTING
# if settings.IS_DEV:
#     import app.tools.arbitrary_script