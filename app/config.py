from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./data/joao_ramos_consultas_database.db"
    ADMIN_USERNAME: str = "joaoramos"
    ADMIN_PASSWORD: str = "joaoramosadminsenha123"
    IS_DEV: bool = False # Valor defaut é false para evitar erros

    class Config:
        env_file = ".env"

settings = Settings()