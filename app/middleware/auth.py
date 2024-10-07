from fastapi import Request, HTTPException, Depends
import jwt
import jwt.api_jwt
from ..config import config, Environment

def auth_artist(request: Request):
    if  config.env == Environment.DEVELOPMENT:
        return
    
    artist_id = request.path_params.get("artist_id")
    if artist_id is None:
        raise HTTPException(status_code=400, detail="Bad request")
    
    if "Authorization" not in request.headers:
        raise HTTPException(status_code=401, detail="Unauthorized")
    token = request.headers.get("Authorization").split("Bearer ")[1]
    
    try:
        payload = jwt.api_jwt.decode(token, config.jwt_secret_key, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
    if payload["sub"] != artist_id:
        raise HTTPException(status_code=403, detail="Forbidden")
    return

def auth_venue(request: Request):
    if  config.env == Environment.DEVELOPMENT:
        return
    
    venue_id = request.path_params.get("venue_id")
    if venue_id is None:
        raise HTTPException(status_code=400, detail="Bad request")
    
    if "Authorization" not in request.headers:
        raise HTTPException(status_code=401, detail="Unauthorized")
    token = request.headers.get("Authorization").split("Bearer ")[1]
    token = request.headers.get("Authorization").split("Bearer ")[1]
    
    try:
        payload = jwt.api_jwt.decode(token, config.jwt_secret_key, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
    if payload["sub"] != venue_id:
        raise HTTPException(status_code=403, detail="Forbidden")
    return