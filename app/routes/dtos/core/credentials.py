from pydantic import BaseModel
from datetime import datetime

class MFARequestModel(BaseModel):
    username: str # AQUI username é utilizado no lugar das informações do dispositivo
    code: str

class MFAResponseModel(BaseModel):
    access_token: str
    mfa_code: str
    mfa_expires_at: datetime
    token_type: str = "bearer"

class UserLoginCredentials(BaseModel):
    username: str
    password: str