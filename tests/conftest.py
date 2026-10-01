import os
import pytest

os.environ["IS_TEST"] = "True"

from fastapi.testclient import TestClient
from app.main import app
from app.config import settings
from app.database.database import get_session

@pytest.fixture(scope="function")
def client():
    with TestClient(app) as test_client:
        yield test_client
    

@pytest.fixture(scope="session", autouse=True)
def delete_db():
    db_url = settings.TARGET_DATABASE_URL
    if db_url.startswith("sqlite:///"):
        db_path = db_url.replace("sqlite:///", "")
        print(f"\n[INFO] Deletando banco de teste...")
        
        if os.path.exists(db_path):
            os.remove(db_path)
            print(f"\n[INFO] Banco de dados de teste deletado: {db_path}")
        else:
            print(f"\n[INFO] Banco de dados não encontrado em: {db_path}")
