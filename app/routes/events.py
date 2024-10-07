from typing import List, Optional, Annotated
from fastapi import APIRouter, HTTPException
from pydantic import Field

from ..models.common import Event
from ..mongo import events_db

router = APIRouter(
    tags=['Event'],
    responses={404: {"description": "Not found"}},
)

@router.get('/event/{artist_id}', response_model=Event)
async def get_event(artist_id: str) -> Event:
    try:
        event_data = await events_db.find_one({"artist_id": artist_id})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while retrieving the event: {str(e)}")
    if event_data is None:
        raise HTTPException(status_code=404, detail="Event not found")
    return event_data


@router.put('/event/{artist_id}', response_model=None)
async def post_event(artist_id: str, event: Event = ...) -> dict:
    try:
        await events_db.update_one({"artist_id": artist_id }, event.model_dump(exclude={"artist_id"}))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while updating the event: {str(e)}")
    return {"message": "Event updated successfully"}


@router.get('/event', response_model=List[Event])
async def get_events(
    venues: Optional[List[str]] = None,
    artists: Optional[List[str]] = None,
    limit: Optional[Annotated[int, Field(ge=1, le=100)]] = 5,
    offset: Optional[Annotated[int, Field(ge=0)]] = 0,
) -> List[Event]:
    pass