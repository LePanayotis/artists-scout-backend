from enum import Enum

class Environment(Enum):
    DEVELOPMENT = 'development'
    TESTING = 'testing'
    PRODUCTION = 'production'

class Config:
    env = Environment.DEVELOPMENT
    jwt_secret_key = "secret" ##IMPORT FROM ENVIRONMENT VARIABLE

    profile_pic_base_url = "http://127.0.0.1:8000/profile_pic"
    song_base_url = "http://127.0.0.1:8000/song"
    mongo_url = 'mongodb://127.0.0.1:27017'
    mongo_main_db = 'artist-scout'
    server_address = '127.0.0.1'
    port = 8000
    


    def __init__(self, 
                 env: Environment = Environment.DEVELOPMENT, 
                 jwt_secret_key: str = "secret",
                 ):
        self.env = env
        self.jwt_secret_key = jwt_secret_key


config = Config(env=Environment.DEVELOPMENT)