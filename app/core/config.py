import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List

load_dotenv()


ENV = os.getenv("ENV", 'dev')

env_file = '.env' if ENV == 'dev' else None

class Settings(BaseSettings):
    ENV: str
    DATABASE_URL: str
    SECRET_KEY: str
    GITHUB_CLIENT_ID : str
    GITHUB_CLIENT_SECRET : str
    GOOGLE_CLIENT_ID : str
    GOOGLE_CLIENT_SECRET : str
    ALGORITHM : str
    ACCESS_TOKEN_EXPIRE_MINUTES : int
    DEBUG: bool = False

    model_config = SettingsConfigDict(
        env_file=env_file,
        extra='ignore'
    )



settings = Settings()

# # Database
# DATABASE_URL = os.getenv('DATABASE_URL')

# # GitHub OAuth
# GITHUB_CLIENT_ID = os.getenv('GITHUB_CLIENT_ID')
# GITHUB_CLIENT_SECRET = os.getenv('GITHUB_CLIENT_SECRET')

# # Google OAuth
# GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
# GOOGLE_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')

# # JWT Credentials
# SECRET_KEY = os.getenv('SECRET_KEY')
# ALGORITHM = os.getenv('ALGORITHM')
# ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

