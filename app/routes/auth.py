from fastapi import APIRouter, HTTPException

from ..mongo import artists_db, venues_db
from ..models.artist import Artist, ArtistPostModel
from ..models.venue import Venue
from ..models.auth import AuthModel, AuthResponse

router = APIRouter(
    tags=['Auth'],
    responses={404: {"description": "Not found"}},
)

@router.post('/login', response_model=AuthResponse)
async def login(type: str = ..., credentials: AuthModel =  ...)->AuthResponse:
    if type == "artist":
        artist = await artists_db.find_one({"email": credentials.email, "password": credentials.password}, {"password": 0})
        if artist is None:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        return AuthResponse(artist)
    elif type == "venue":
        venue = await venues_db.find_one({"email": credentials.email, "password": credentials.password}, {"password": 0})
        if venue is None:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        return AuthResponse(venue)
    else:
        raise HTTPException(status_code=400, detail="Invalid login type")