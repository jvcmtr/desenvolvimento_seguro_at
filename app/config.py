from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./data/joao_ramos_consultas_database.db"
    TEST_DATABASE_URL: str = "sqlite:///./data/test_database.db"
    ADMIN_USERNAME: str = "joaoramos"
    ADMIN_PASSWORD: str = "joaoramosadminsenha123"
    
    JWT_ENCODE_KEY : str = "CHAVE_USADA_PARA_ENCRIPTAR_O_JWT_CONFIGURE_UMA_SEGURA_EM_.env"
    SYSTEM_USER_ID:int  = 1
    
    # Valor defaut é false para evitar erros
    IS_DEV : bool = False
    IS_TEST: bool = False

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    @property
    def TARGET_DATABASE_URL(self) -> str:
        if self.IS_TEST:
            return self.TEST_DATABASE_URL
        return self.DATABASE_URL

settings = Settings()