from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.controllers.misc_controller import router as MISC_ROUTER

app = FastAPI()

# CONFIG
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/documents", StaticFiles(directory="docs"), name="documents")

# Extremamente inseguro pois permite verificar __pycache__
app.mount("/sourcecode", StaticFiles(directory="app"), name="app") 

# ROUTERS
app.include_router(MISC_ROUTER)