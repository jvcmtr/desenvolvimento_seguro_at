import time
from fastapi import Request, status
from app.config import settings

MAX_ATTEMPTS = settings.LOGIN_MAX_ATTEMPTS
WINDOW_SECONDS = LOGIN_ATTEMPTS_TIMESPAN_MINUTES * 60

LOGIN_ATTEMPT_STORE: dict[str, list[float]] = {}

def check_login_rate_limit(request: Request):
    client_ip = request.client.host if request.client else "unknown"
    now = time.time()
    
    if client_ip not in LOGIN_ATTEMPT_STORE:
        LOGIN_ATTEMPT_STORE[client_ip] = []
        
    # Remove tentativas fora da janela de tempo
    LOGIN_ATTEMPT_STORE[client_ip] = [t for t in LOGIN_ATTEMPT_STORE[client_ip] if now - t < WINDOW_SECONDS]
    
    if len(LOGIN_ATTEMPT_STORE[client_ip]) >= MAX_ATTEMPTS:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Muitas tentativas de login. Tente novamente mais tarde."
        )
        
    LOGIN_ATTEMPT_STORE[client_ip].append(now)