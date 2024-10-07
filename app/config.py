from enum import Enum

class Environment(Enum):
    DEVELOPMENT = 'development'
    TESTING = 'testing'
    PRODUCTION = 'production'

class Config:
    env = Environment.DEVELOPMENT
    jwt_secret_key = "secret" ##IMPORT FROM ENVIRONMENT VARIABLE

    def __init__(self, env: Environment = Environment.DEVELOPMENT, jwt_secret_key: str = "secret"):
        self.env = env
        self.jwt_secret_key = jwt_secret_key
config = Config(env=Environment.DEVELOPMENT)