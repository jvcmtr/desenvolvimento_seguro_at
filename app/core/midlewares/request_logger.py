import time
from fastapi import Request
from app.core.log_config import logger
from app.core.auth import oauth2_scheme, decode_jwt

def register_request_logger(app):
    @app.middleware("http")
    async def log_requests(request: Request, call_next):
        
        response = await call_next(request)
        sub = "anonymous user"
        credentials = "NULL"
        try:
            credentials = await oauth2_scheme(request)
            data = decode_jwt(credentials.credentials)
            sub = data.get("sub", "anonymous user")
            sub += f" (id={data.get("user_id", "LAB_CLIENT")})"
        except:
            pass

        logger.info(f"Method: {request.method} | Path: {request.url.path} | Status: {response.status_code} | User: {sub} | Credentials: {credentials}")
        return response