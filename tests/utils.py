from sqlmodel import Session
from app.database.database import engine
from app.config import settings
from app.core.auth import get_password_hash
from app.models.core.Users import User


def add_user_to_db(user : User):
    user.password = get_password_hash(user.password)
    with Session(engine) as session:
        session.add(user)
        session.commit()
        session.refresh(user)

    return user

def remove_user_from_db(user : User):
    with Session(engine) as session:
        u = session.get(User, user.id)
        if u:
            session.delete(u)
            session.commit()
            return True
        else:
            return False

def login_as(client, username, password):
    response = client.post("/auth/login", json={"username":username, "password":password})
    if not response.status_code == 200:
        raise AssertionError( f"Failed to login. STATUS: {response.status_code}. RESPONSE: {response.text}")

    login_resp = response.json()
    jwt = login_resp["access_token"]
    mfa = login_resp["mfa_code"]

    response = client.post("/auth/confirm-mfa", json={"username":username, "code":mfa })
    if not response.status_code == 200:
        raise AssertionError( f"Failed to verify MFA. STATUS: {response.status_code}. RESPONSE: {response.text}")

    client.headers.update({
        "Authorization": f"Bearer {jwt}"
    })

def login_as_adm(client):
    return login_as(client, settings.ADMIN_USERNAME, settings.ADMIN_PASSWORD)

def logout(client):
    client.headers.pop("Authorization", None)

    