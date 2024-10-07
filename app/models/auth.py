from pydantic import BaseModel, EmailStr, Field
from typing import Optional, Annotated

from ..config import config
from .venue import Venue
from .artist import Artist
import  jwt


class AuthModel(BaseModel):
    email: EmailStr = Field(...)
    password: str = Field(...)
    
    class Config:
        json_encoders = {
            EmailStr: str
        }

class AuthResponse(BaseModel):
    token: str
    id: str

    def __init__(self, artist: Artist):
        self.token = jwt.encode({"venue_id": artist.artist_id}, config.jwt_secret_key, algorithm="HS256", )
        self.id = artist.artist_id
    
    def __init__(self, venue: Venue):
        self.token = jwt.encode({"venue_id": venue.venue_id}, config.jwt_secret_key, algorithm="HS256")
        self.id = venue.venue_id