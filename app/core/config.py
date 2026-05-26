import os
from dotenv import load_dotenv

load_dotenv()


ENV = os.getenv("ENV", 'dev')
DEBUG = ENV == 'dev'


# Database
DATABASE_URL = os.getenv('DATABASE_URL')
GITHUB_CLIENT_ID = os.getenv('GITHUB_CLIENT_ID')
GITHUB_CLIENT_SECRET = os.getenv('GITHUB_CLIENT_SECRET')

GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
GOOGLE_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')