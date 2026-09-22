from pydantic import BaseModel
from datetime import datetime
from app.models.core.Users import UserRole, User

# Mesmo com a separação em camadas/modulos, ainda é interessante manter 
# os DTOs separados dos demais modelos de banco de dados. 
 
class UserViewModel(BaseModel):
    id: int
    username: str
    role: UserRole
    created_at: datetime # dt criação do usuario ainda é visivel, demais campos de auditoria não

    @classmethod
    def create_from(cls, user: User) -> "UserViewModel":
        return cls(**user.__dict__)


class UserPostModel(BaseModel):
    id : int | None = None
    username: str
    password: str
    role: UserRole 

    def as_model(self) -> User:
        return User(**self.__dict__)

    def update(self, user) -> User:
        user.username = self.username
        user.password = self.password
        user.role = self.role

        user.updated_at = datetime.date()
        user.updated_by = self.username
        user.updated_by_user_id = self.id
        
        return user