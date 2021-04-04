import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Set Flask configuration variables"""

    SECRET_KEY = os.environ.get('SECRET_KEY')
    TESTING = os.environ.get('TESTING')
    DEBUG = os.environ.get('DEBUG')
