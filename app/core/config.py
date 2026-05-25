import os
from dotenv import load_dotenv

load_dotenv()


ENV = os.getenv("ENV", 'dev')
DEBUG = ENV == 'dev'


# Database
DATABASE_URL = os.getenv('DATABASE_URL')
