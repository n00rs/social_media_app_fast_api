from pydantic.v1 import BaseSettings

''' create and class by extending BaseSettings
    to load environment variables from .env file
'''
class Settings(BaseSettings):
    database_host:str
    database_password:str
    database_name:str
    database_port:str
    database_username:str
    secret_key:str
    algorithm:str
    access_token_expire_minutes:int
    
    class Config:
        env_file = ".env"
    
    
settings = Settings()
