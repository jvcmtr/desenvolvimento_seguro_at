from sqlmodel import Session, select
import os

from app.config import settings
from app.database.database import create_db_and_tables
from .create_hash import hash_pass
from .create_admin import create_admin_user, get_user_and_password_input

def setup_db(username = None, password = None):
    if settings.DATABASE_URL.startswith("sqlite:///"):
        os.makedirs(os.path.dirname(os.path.abspath(settings.DATABASE_URL.replace("sqlite:///", ""))), exist_ok=True)

    username = username or settings.ADMIN_USERNAME
    password = password or settings.ADMIN_PASSWORD
    
    create_db_and_tables()
    create_admin_user(username, password)

def main():
    username, password = get_user_and_password_input() 
    setup_db(username, password)


if __name__ == "__main__":
    main()