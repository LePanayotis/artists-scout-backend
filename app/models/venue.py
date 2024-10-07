from __future__ import annotations

from datetime import date, datetime, time
from enum import Enum
from typing import List, Optional, Annotated
from bson import ObjectId
from pydantic import AfterValidator, HttpUrl, BaseModel, EmailStr, Field
from ..utils.utils import generate_random_id

from .common import ArtType, VenueType, Address, Event

      
class VenueBaseModel(BaseModel):
    name: str = Field(...)
    about: Optional[str] = None
    email: EmailStr = Field(...)
    phone: Annotated[str, Field(pattern=r'^[+]?[0-9]*$')]
    address: Address = None
    coordinates: str = None
    venue_type: VenueType = Field(...)
    art_type: Optional[ArtType] = None
    last_modified: Optional[datetime] = datetime.now()
    
    class Config:
        use_enum_values = True
        json_encoders = {
            HttpUrl: str,
            EmailStr: str
        }

class VenuePostModel(VenueBaseModel):
    password: str = Field(...)

class Venue(VenuePostModel):
    venue_id: str = generate_random_id()
    venue_pic: Optional[str] = None
    password: Optional[str] =   None