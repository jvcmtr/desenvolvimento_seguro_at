from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./data/joao_ramos_consultas_database.db"
    TEST_DATABASE_URL: str = "sqlite:///./data/test_database.db"
    
    ADMIN_USERNAME: str = "joaoramos"
    ADMIN_PASSWORD: str = "joaoramosadminsenha123"
    SYSTEM_USER_ID:int  = 1
    
    JWT_ENCODE_KEY : str = "CHAVE_USADA_PARA_ENCRIPTAR_O_JWT_CONFIGURE_UMA_SEGURA_EM_.env"
    USER_JWT_EXPIRES_IN_MINUTES : int = 60 * 12 # 12h
    MFA_EXPIRE_MINUTES: int = 2

    LAB_CLIENT_ID: str = "laboratorio_parceiro_id"
    LAB_CLIENT_SECRET: str = "laboratorio_parceiro_secret"
    LAB_REQUIRED_SCOPE: str = "lab_access"
    LAB_JWT_EXPIRES_IN_MINUTES : int = 60 * 12 # 48h

    LOG_LEVEL_STDOUT: str = "DEBUG"
    LOG_LEVEL_FILE: str = "INFO"
    LOG_FILE_PATH: str = "./data/joao_ramos_app.log"
    TEST_LOG_FILE_PATH: str = "./data/joao_ramos_app.test.log"

    
    # Valor defaut é false para evitar erros
    IS_DEV : bool = False
    IS_TEST: bool = False

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    @property
    def TARGET_DATABASE_URL(self) -> str:
        if self.IS_TEST:
            return self.TEST_DATABASE_URL
        return self.DATABASE_URL

    @property
    def TARGET_LOG_FILE_PATH(self) -> str:
        if self.IS_TEST:
            return self.TEST_LOG_FILE_PATH
        return self.LOG_FILE_PATH

settings = Settings()