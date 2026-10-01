from pydantic import BaseModel

class M2MLoginResponseModel(BaseModel):
    access_token: str
    expires_in: int
    scope:str
    token_type: str = "bearer"