import os


class Config:
    """Set Flask configuration variables"""

    FLASK_ENV = os.getenv('FLASK_ENV', 'production')
    SECRET_KEY = os.getenv('FLASK_SECRET', 'Secret')
