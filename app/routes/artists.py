import asyncio
import os
from datetime import datetime
from typing import List, Optional
from fastapi import APIRouter, HTTPException, Depends, Request


from ..middleware.auth import auth_artist
from ..models.common import ArtType, Event
from ..mongo import artists_db, events_db
from ..models.artist import Artist, ArtistPostModel

router = APIRouter(
    tags=['Artist'],
    responses={404: {"description": "Not found"}},
)

profile_pic_base_url = "http://127.0.0.1:8000/profile_pic"
song_base_url = "http://127.0.0.1:8000/song"



@router.post('/artist', response_model=Artist, response_model_exclude={"password"})
async def post_artist(artist: ArtistPostModel =  ...)->Artist:
    artist = Artist(**artist.model_dump())
    event = Event(artist_id=artist.artist_id)
    try:
        existing = await artists_db.find_one({"email": artist.email})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while checking for existing artist: {str(e)}")
    if existing is not None:
        raise HTTPException(status_code=409, detail="Artist with this email already exists")
    try:
        await asyncio.gather(
            artists_db.insert_one(artist.model_dump()),
            events_db.insert_one(event.model_dump())
        )
    except Exception as e:
        await asyncio.gather(
            artists_db.delete_one({"artist_id": artist.artist_id}),
            events_db.delete_one({"artist_id": artist.artist_id})
        )
        raise HTTPException(status_code=500, detail=f"An error occurred while creating the artist: {str(e)}")
    return artist

@router.get('/artist/{artist_id}', response_model=Artist, response_model_exclude={"password"})
async def get_artist(artist_id: str) -> Artist:
    try:
        artist_data = await artists_db.find_one({"artist_id": artist_id}, {"password": 0})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while retrieving the artist: {str(e)}")
    if artist_data is None:
        raise HTTPException(status_code=404, detail="Artist not found")
    if artist_data["sample_song"]:
        artist_data["sample_song"]["audio_file"] = f"{song_base_url}/{artist_id}"
    if artist_data["profile_pic"]:
        artist_data["profile_pic"] = f"{profile_pic_base_url}/{artist_id}"
    return artist_data


@router.put('/artist/{artist_id}', response_model=None, dependencies=[Depends(auth_artist)])
async def put_artist(artist_id: str, artist: dict) -> None:
    immutable_fields = {"artist_id", "profile_pic", "sample_song"}
    update_fields = {key: artist[key] for key in artist.keys() if key in Artist.model_fields and key not in immutable_fields}
    if update_fields:
        update_fields["last_modified"] = datetime.now()
    try:
        await artists_db.update_one({"artist_id": artist_id}, {"$set": update_fields})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while updating the artist: {str(e)}")
    return {"message": "Artist updated successfully"}


@router.delete('/artist/{artist_id}', response_model=None, dependencies=[Depends(auth_artist)])
async def delete_artist(artist_id: str) -> None:
    try:
        await asyncio.gather(
            artists_db.delete_one({"artist_id": artist_id}),
            events_db.delete_one({"artist_id": artist_id})
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while deleting the artist: {str(e)}")
    return {"message": "Artist deleted successfully"}


### TODO: Implement the get_artists endpoint

@router.get('/artist', response_model=List[Artist])
async def get_artists(
    art_type: Optional[List[ArtType]] = None,
    genres: Optional[List[str]] = None,
    center: Optional[str] = None,
    max_distance: Optional[float] = None
) -> List[Artist]:
    pass
