from __future__ import annotations
import asyncio
from datetime import datetime
from typing import List, Optional
from fastapi import APIRouter, HTTPException, Depends


from ..models.venue import Venue, VenuePostModel
from ..models.common import ArtType, VenueType, ReturnMessage
from ..mongo import venues_db, events_db
from ..middleware.auth import auth_venue

router = APIRouter(
    tags=['Venue'],
    responses={404: {"description": "Not found"}},
)

@router.post('/venue', response_model=Venue, response_model_exclude={"password"})
async def post_venue(venue: VenuePostModel = ...) -> Venue:
    try:
        existing = await venues_db.find_one({"email": venue.email})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while checking for existing venue: {str(e)}")
    if existing is not None:
        raise HTTPException(status_code=409, detail="Venue with this email already exists")
    try:
        venue = Venue(**venue.model_dump())
        await venues_db.insert_one(venue.model_dump())
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while creating the venue: {str(e)}")
    return venue


@router.get('/venue/{venue_id}', response_model=Venue, response_model_exclude={"password"})
async def get_venue(venue_id: str) -> Venue:
    try:
        venue_data = await venues_db.find_one({"venue_id": venue_id}, {"password": 0})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while retrieving the venue: {str(e)}")
    if venue_data is None:
        raise HTTPException(status_code=404, detail="Venue not found")
    return venue_data



@router.put('/venue/{venue_id}', response_model=ReturnMessage, dependencies=[Depends(auth_venue)])
async def put_venue(venue_id: str, body: dict = ...) -> ReturnMessage:
    update_fields = {key: body[key] for key in body.keys() if key in Venue.model_fields and key not in {"venue_id", "venue_pic"}}
    if update_fields:
        update_fields["last_modified"] = datetime.now()
    try:
        await venues_db.update_one({"venue_id": venue_id}, {"$set": update_fields})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while updating the venue: {str(e)}")
    return ReturnMessage(message="Venue updated successfully")


@router.delete('/venue/{venue_id}', response_model=ReturnMessage, dependencies=[Depends(auth_venue)])
async def delete_venue(venue_id: str) -> ReturnMessage:
    try:
        await asyncio.gather(
            await venues_db.delete_one({"venue_id": venue_id}),
            await events_db.update_many({"venue_id": venue_id}, {"$set": {"venue_id": None, "date": None, "time": None, "title": None}})
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while deleting the venue: {str(e)}")
    return ReturnMessage(message="Venue deleted successfully")


@router.get('/venue', response_model=List[Venue])
async def get_venues(
    venue_type: Optional[List[VenueType]] = None,
    art_type: Optional[List[ArtType]] = None,
    center: Optional[str] = None,
    radius: Optional[float] = None,
) -> List[Venue]:
    pass