import motor.motor_asyncio

from .config import config

client = motor.motor_asyncio.AsyncIOMotorClient(config.mongo_url)

database = client[config.mongo_main_db]

venues_db = database.get_collection('venues')
artists_db = database.get_collection('artists')
events_db = database.get_collection('events')