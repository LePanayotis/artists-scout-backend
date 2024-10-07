from __future__ import annotations

from datetime import date, datetime, time
from enum import Enum
from typing import List, Optional, Annotated
from pydantic import AfterValidator, HttpUrl, BaseModel, EmailStr, Field
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
    audio_file: HttpUrl
    title: str
    
    class Config:
        json_encoders = {
            HttpUrl: str
        }

class ReturnMessage(BaseModel):
    message: Optional[str] = None
    code: Annotated[int,Field(..., ge=200, le=599)] = 200