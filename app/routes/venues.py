from __future__ import annotations

from datetime import datetime
from typing import List, Optional
from fastapi import APIRouter, HTTPException


from ..models.schemata import Venue, ArtType, VenueType
from ..mongo import venues_db

router = APIRouter(
    tags=['Venue'],
    responses={404: {"description": "Not found"}},
)

@router.post('/venue', response_model=None)
async def post_venue(venue: Venue = ...) -> None:
    try:
        existing = await venues_db.find_one({"email": venue.email})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while checking for existing venue: {str(e)}")
    if existing is not None:
        raise HTTPException(status_code=409, detail="Venue with this email already exists")
    try:
        await venues_db.insert_one(venue.model_dump())
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while creating the venue: {str(e)}")
    return {"message": "Venue created successfully"}


@router.get('/venue/{venue_id}', response_model=Venue)
async def get_venue(venue_id: str) -> Venue:
    try:
        venue_data = await venues_db.find_one({"venue_id": venue_id})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while retrieving the venue: {str(e)}")
    if venue_data is None:
        raise HTTPException(status_code=404, detail="Venue not found")
    return venue_data.model_dump()


@router.put('/venue/{venue_id}', response_model=None)
async def put_venue(venue_id: str, body: Venue = ...) -> None:
    update_fields = {key: body[key] for key in body.keys() if key in Venue.model_fields and key not in {"venue_id"}}
    if update_fields:
        update_fields["last_modified"] = datetime.now()
    try:
        await venues_db.update_one({"venue_id": venue_id}, {"$set": update_fields})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while updating the venue: {str(e)}")
    return {"message": "Venue updated successfully"}


@router.delete('/venue/{venue_id}', response_model=None)
async def delete_venue(venue_id: str) -> None:
    ### also set to none events that have this venue_id
    try:
        await venues_db.delete_one({"venue_id": venue_id})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while deleting the venue: {str(e)}")
    return {"message": "Venue deleted successfully"}

@router.get('/venue', response_model=List[Venue])
async def get_venues(
    venue_type: Optional[List[VenueType]] = None,
    art_type: Optional[List[ArtType]] = None,
    center: Optional[str] = None,
    radius: Optional[float] = None,
) -> List[Venue]:
    pass