from __future__ import annotations
from datetime import datetime

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from ..models.schemata import ReturnMessage
from ..mongo import artists_db, venues_db
from fastapi import UploadFile, File
import os
router = APIRouter(
    tags=['Multimedia'],
    responses={404: {"description": "Not found"}},
)

profile_pic_path = "C:\\Users\\ppapa\\Desktop\\Projects\\artists-scout\\static\\profile_pics"
audio_path = "C:\\Users\\ppapa\\Desktop\\Projects\\artists-scout\\static\\audio"
venue_pic_path = "C:\\Users\\ppapa\\Desktop\\Projects\\artists-scout\\static\\venue_pics"

async def find_artist(artist_id: str)->dict:
    try:
        artist = await artists_db.find_one({"artist_id": artist_id})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while retrieving the artist: {str(e)}")
    if artist is None:
        raise HTTPException(status_code=404, detail="Artist not found")
    return artist

async def find_venue(artist_id: str)->dict:
    try:
        venue = await venues_db.find_one({"venue_id": artist_id})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while retrieving the venue: {str(e)}")
    if venue is None:
        raise HTTPException(status_code=404, detail="Venue not found")
    return venue

@router.put('/profile_pic/{artist_id}', response_model=None)
async def post_profile_pic(artist_id: str, img: UploadFile = File(...)) -> ReturnMessage:
    
    file_format = img.filename.split(".")[-1]
    if file_format not in {"jpg", "jpeg", "png"}:
        raise HTTPException(status_code=400, detail="Invalid file format. Only jpg, jpeg and png are allowed")

    artist = await find_artist(artist_id)
    if artist["profile_pic"] is not None:
        if os.path.exists(artist["profile_pic"]):
            os.remove(artist["profile_pic"])
    
    file_location = os.path.join(profile_pic_path, f"{artist_id}.{file_format}")
    with open(file_location, "wb") as f:
        f.write(await img.read())
    try:
        last_modified = datetime.now()
        await artists_db.update_one({"artist_id": artist_id}, {"$set": {"profile_pic": file_location, "last_modified": last_modified}})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while updating the artist profile pic: {str(e)}")
    return ReturnMessage(message="Profile pic uploaded successfully")



@router.get('/profile_pic/{artist_id}', response_model=bytes)
async def get_profile_pic(artist_id: str) -> bytes:
    artist = await find_artist(artist_id)
    if artist["profile_pic"] is None:
        raise HTTPException(status_code=404, detail="Profile pic not found")
    if not os.path.exists(artist["profile_pic"]):
        raise HTTPException(status_code=500, detail="Profile pic not found on server")
    
    file_format = artist["profile_pic"].split(".")[-1]
    if file_format is "jpg":
        file_format = "jpeg"
    return FileResponse(artist["profile_pic"], media_type=f"image/{file_format}")


@router.delete('/profile_pic/{artist_id}', response_model=None)
async def delete_profile_pic(artist_id: str) -> None:
    artist = await find_artist(artist_id)
    if artist["profile_pic"] is not None:
        if os.path.exists(artist["profile_pic"]):
            os.remove(artist["profile_pic"])
        try:
            last_modified = datetime.now()
            await artists_db.update_one({"artist_id": artist_id}, {"$set": {"profile_pic": None, "last_modified": last_modified}})
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"An error occurred while deleting the artist profile pic: {str(e)}")
    return ReturnMessage(message="Profile pic deleted successfully")



@router.put('/song/{artist_id}', response_model=None)
async def post_song(artist_id: str, audio: UploadFile = File(...)) -> ReturnMessage:
    file_format = audio.filename.split(".")[-1]
    song_title = ".".join(audio.filename.split(".")[:-1])
    print(song_title)
    if file_format not in {"mp3"}:
        raise HTTPException(status_code=400, detail="Invalid file format. Only mp3 are allowed")
    
    artist = await find_artist(artist_id)
    if artist["sample_song"] is not None:
        if os.path.exists(artist["sample_song"]["audio_file"]):
            os.remove(artist["sample_song"]["audio_file"])
    
    file_location = os.path.join(audio_path, f"{artist_id}.{file_format}")
    with open(file_location, "wb") as f:
        f.write(await audio.read())
    
    try:
        last_modified = datetime.now()
        await artists_db.update_one({"artist_id": artist_id}, {"$set": {"sample_song": {"audio_file": file_location, "title": song_title}, "last_modified": last_modified}})
    except Exception as e:
        os.remove(file_location)
        raise HTTPException(status_code=500, detail=f"An error occurred while updating the artist song: {str(e)}")
    return ReturnMessage(message="Song uploaded successfully")


@router.get('/song/{artist_id}', response_model=bytes)
async def get_song(artist_id: str) -> bytes:
    artist = await find_artist(artist_id)
    if artist["sample_song"] is None:
        raise HTTPException(status_code=404, detail="Sample song not found")
    if not os.path.exists(artist["sample_song"]["audio_file"]):
        raise HTTPException(status_code=500, detail="Sample song not found on server")
    return FileResponse(artist["sample_song"]["audio_file"], media_type="audio/mpeg")


@router.delete('/song/{artist_id}', response_model=None)
async def delete_song(artist_id: str) -> None:

    artist = await find_artist(artist_id)

    if artist["sample_song"] is not None:
        if os.path.exists(artist["sample_song"]["audio_file"]):
            os.remove(artist["sample_song"]["audio_file"])
        try:
            last_modified = datetime.now()
            await artists_db.update_one({"artist_id": artist_id}, {"$set": {"sample_song": None, "last_modified": last_modified}})	
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"An error occurred while deleting the artist sample song: {str(e)}")
    return ReturnMessage(message="Sample song deleted successfully")


@router.put('/venue_pic/{venue_id}', response_model=None)
async def post_profile_pic(venue_id: str, img: UploadFile = File(...)) -> ReturnMessage:
    
    file_format = img.filename.split(".")[-1]
    if file_format not in {"jpg", "jpeg", "png"}:
        raise HTTPException(status_code=400, detail="Invalid file format. Only jpg, jpeg and png are allowed")
    
    await find_venue(venue_id)
    
    file_location = os.path.join(venue_pic_path, f"{venue_id}.{file_format}")
    with open(file_location, "wb") as f:
        f.write(await img.read())
    try:
        last_modified = datetime.now()
        await artists_db.update_one({"venue_id": venue_id}, {"$set": {"venue_pic": file_location, "last_modified": last_modified}})
    except Exception as e:
        os.remove(file_location)
        raise HTTPException(status_code=500, detail=f"An error occurred while updating the venue pic: {str(e)}")
    return ReturnMessage(message="Venue pic uploaded successfully")



@router.get('/venue_pic/{venue_id}', response_model=bytes)
async def get_profile_pic(venue_id: str) -> bytes:
    venue = await find_venue(venue_id)
    if venue["venue_pic"] is None:
        raise HTTPException(status_code=404, detail="Venue pic not found")
    if not os.path.exists(venue["venue_pic"]):
        raise HTTPException(status_code=500, detail="Venue pic not found on server")
    
    file_format = venue["venue_pic"].split(".")[-1]
    if file_format is "jpg":
        file_format = "jpeg"
    return FileResponse(venue["venue_pic"], media_type=f"image/{file_format}")


@router.delete('/venue_pic/{venue_id}', response_model=None)
async def delete_profile_pic(venue_id: str) -> None:
    venue = await find_venue(venue_id)
    if venue["venue_pic"] is not None:
        if os.path.exists(venue["venue_pic"]):
            os.remove(venue["venue_pic"])
        try:
            last_modified = datetime.now()
            await venues_db.update_one({"venue_id": venue_id}, {"$set": {"venue_pic": None, "last_modified": last_modified}})
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"An error occurred while deleting the venue pic: {str(e)}")
    return ReturnMessage(message="Venue pic deleted successfully")