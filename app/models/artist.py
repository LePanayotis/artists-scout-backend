from __future__ import annotations

from datetime import date, datetime, time
from enum import Enum
from typing import List, Optional, Annotated
from pydantic import AfterValidator, HttpUrl, BaseModel, EmailStr, Field
from ..utils.utils import generate_random_id

from .common import ArtType, VenueType, Address, Event, SampleSong

class ArtistBaseModel(BaseModel):
    name: str = Field(...)
    about: Optional[str] = None
    city: Optional[str] = None
    coordinates: Optional[str] = None
    art_type: ArtType = Field(...)
    genres: Optional[List[str]] = None
    email: EmailStr = Field(...)
    phone: Optional[Annotated[str, Field(pattern=r'^[+]?[0-9]*$', max_length=15)]] = None
    spotify: Optional[Annotated[HttpUrl, AfterValidator(lambda v: str(v))]] = None
    youtube: Optional[Annotated[HttpUrl, AfterValidator(lambda v: str(v))]] = None
    last_modified: Optional[datetime] = datetime.now()

    class Config:
        use_enum_values = True
        json_encoders = {
            HttpUrl: str,
            EmailStr: str
        }

class ArtistPostModel(ArtistBaseModel):
    password: str = Field(...)

class Artist(ArtistPostModel):
    artist_id: str = generate_random_id()
    profile_pic: Optional[str] = None
    sample_song: Optional[SampleSong] = None
    password: Optional[str] =   None