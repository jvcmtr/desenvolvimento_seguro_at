from sqlmodel import Session, select

from app.config import settings
from app.database.database import engine
from app.models.core.Users import User, UserRole
from .create_hash import hash_pass

def get_user_and_password_input():
    skip = input(f"Deseja utilizar o usuario padrão '{settings.ADMIN_USERNAME}'? (y/n)").lower()
    if skip == 'y':
        return settings.ADMIN_USERNAME, settings.ADMIN_PASSWORD 

    username = input("Digite o nome do usuario admin: ").strip()
    password = input(f"Digite a senha para o usuario '{username}': ")
    password2 = input(f"Confirme sua senha: ")

    if len(username < 3):
        print("ERRO: nome de usuario deve conter pelo menos 3 caracteres")
        raise "USUARIO ADMIN COM ERRO"

    if len(password < 3):
        print("ERRO: senha deve conter pelo menos 3 caracteres")
        raise "USUARIO ADMIN COM ERRO"

    if password != password2:
        print("ERRO: As senhas fornescidas não são identicas")
        raise "USUARIO ADMIN COM ERRO"
    
    return username, hash_pass(password)


def create_admin_user(username, password):
    if not username or not password:
        print("[ERRO] usuario ou senha invalidos")
        return

    with Session(engine) as session:
        statement = select(User).where(User.username == username)
        existing_user = session.exec(statement).first()

        if existing_user:
            print(f"[WARNING] Já existe um usuario com o username='{username}' no banco de dados.")
            return

        admin_user = User(
            username=username,
            password=hash_pass(password),
            role=UserRole.ADMIN,
            created_by=username,
            created_by_user_id=settings.SYSTEM_USER_ID
        )

        session.add(admin_user)
        session.commit()
        print(f"[INFO] Usuário admin '{username}' [ID={admin_user.id}] criado com sucesso")

def main():
    username, password = get_user_and_password_input() 
    create_admin_user(username, password)

if __name__ == "__main__":
    main()