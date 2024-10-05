import motor.motor_asyncio

### Download and create your own mongo instance
MONGO_DETAILS = 'mongodb://127.0.0.1:27017'

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)

database = client['artist-scout']

venues_db = database.get_collection('venues')
artists_db = database.get_collection('artists')
events_db = database.get_collection('events')