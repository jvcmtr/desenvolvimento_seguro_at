from app.config import settings
from pydantic import BaseModel
from datetime import datetime

# ESTE MODELO NÃO FICA SALVO NO BANCO DE DADOS !!!

class MFAMetadata(BaseModel):
    dispositivo: str   # AQUI username é utilizado no lugar das informações do dispositivo
    user_id: int 
    code: str
    expires_at: datetime
    confirmed: bool 