from fastapi import Request, HTTPException, Header
import jwt
import jwt.api_jwt
from ..config import config, Environment

def auth_artist(Authorization: str = Header(None), artist_id: str = ...):
    if config.env == Environment.DEVELOPMENT:
        return
    print(Authorization, artist_id)
    if artist_id is None:
        raise HTTPException(status_code=400, detail="Bad request")
    
    if Authorization is None:
        raise HTTPException(status_code=401, detail="Unauthorized")
    token = Authorization.split("Bearer ")[1]
    
    try:
        payload = jwt.api_jwt.decode(token, config.jwt_secret_key, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
    if payload["sub"] != artist_id:
        raise HTTPException(status_code=403, detail="Forbidden")
    return

def auth_venue(Authorization: str = Header(None), venue_id: str = ...):
    if config.env == Environment.DEVELOPMENT:
        return
    if venue_id is None:
        raise HTTPException(status_code=400, detail="Bad request")
    
    if Authorization is None:
        raise HTTPException(status_code=401, detail="Unauthorized")
    token = Authorization.split("Bearer ")[1]
    
    try:
        payload = jwt.api_jwt.decode(token, config.jwt_secret_key, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
    if payload["sub"] != venue_id:
        raise HTTPException(status_code=403, detail="Forbidden")
    return
