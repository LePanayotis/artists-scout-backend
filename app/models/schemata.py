# generated by fastapi-codegen:
#   filename:  .\artist-scout-oas.yaml
#   timestamp: 2024-10-03T19:37:18+00:00

from __future__ import annotations

from datetime import date, datetime, time
from enum import Enum
from typing import List, Optional, Annotated
from bson import ObjectId
from pydantic import AnyUrl, BaseModel, EmailStr, Field
from ..utils.utils import generate_random_id

class ArtType(str, Enum):
    painting = 'painting'
    sculpture = 'sculpture'
    music = 'music'
    dance = 'dance'
    theater = 'theater'
    photography = 'photography'
    digital_art = 'digital_art'
    other = 'other'

class VenueType(str, Enum):
    bar = 'bar'
    cafe = 'cafe'
    restaurant = 'restaurant'
    gallery = 'gallery'
    museum = 'museum'
    shop = 'shop'
    park = 'park'
    other = 'other'

class Address(BaseModel):
    street: str
    city: str
    postal_code: str
    country: str

class Event(BaseModel):
    title: Optional[str] = None
    artist_id: Optional[str] = None
    venue_id: Optional[str] = None
    date: Optional[date] = None
    time: Optional[time] = None
    last_modified: Optional[datetime] = datetime.now()

class SampleSong(BaseModel):
    audio_file: AnyUrl
    title: str
    
    class Config:
        json_encoders = {
            AnyUrl: str
        }

class Artist(BaseModel):
    artist_id: Optional[str] = generate_random_id()
    name: str = Field(...)
    about: Optional[str] = None
    city: Optional[str] = None
    coordinates: Optional[str] = None
    art_type: ArtType = Field(...)
    genres: Optional[List[str]] = None
    profile_pic: Optional[AnyUrl] = None
    sample_song: Optional[SampleSong] = None
    email: EmailStr = Field(...)
    password: str = Field(...)
    phone: Optional[Annotated[str, Field(pattern=r'^[+]?[0-9]*$', max_length=15)]] = None
    spotify: Optional[AnyUrl] = None
    youtube: Optional[AnyUrl] = None
    last_modified: Optional[datetime] = datetime.now()

    class Config:
        use_enum_values = True
        json_encoders = {
            AnyUrl: str,
            EmailStr: str
        }

class Venue(BaseModel):
    venue_id: Optional[str] = generate_random_id()
    name: Optional[str] = Field(...)
    about: Optional[str] = None
    email: Optional[EmailStr] = Field(...)
    phone: Optional[Annotated[str, Field(pattern=r'^[+]?[0-9]*$')]]
    address: Optional[Address] = None
    coordinates: Optional[str] = None
    venue_type: Optional[VenueType] = None
    art_type: Optional[ArtType] = None
    venue_pic: Optional[AnyUrl] = None
    upcoming_events: Optional[List[Event]] = None
    last_modified: Optional[datetime] = datetime.now()

class ReturnMessage(BaseModel):
    message: Optional[str] = None
    code: Annotated[int,Field(..., ge=200, le=599)] = 200