from pydantic import BaseModel

class MFARequestModel(BaseModel):
    username: str # AQUI username é utilizado no lugar das informações do dispositivo
    code: str