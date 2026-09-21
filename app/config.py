from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./data/joao_ramos_consultas_database.db"
    ADMIN_USERNAME: str = "joaoramos"
    ADMIN_PASSWORD: str = "joaoramosadminsenha123"
    IS_DEV: bool = False # Valor defaut é false para evitar erros

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings()