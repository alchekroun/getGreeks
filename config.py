import os
import sys


class Config:
    """Set Flask configuration variables"""

    FLASK_ENV = os.getenv('FLASK_ENV', 'production')
    SECRET_KEY = os.getenv('FLASK_SECRET', 'Secret')

    """
    APP_DIR = os.path.dirname(__file__)
    print(">>>>>>" + APP_DIR, file=sys.stdout)
    ROOT_DIR = os.path.dirname(APP_DIR)
    print(">>>>>>" + ROOT_DIR, file=sys.stdout)
    DIST_DIR = os.path.join(APP_DIR, 'dist')
    print(">>>>>>" + DIST_DIR, file=sys.stdout)

    if not os.path.exists(DIST_DIR):
        raise Exception(
            'DIST_DIR not found: {}'.format(DIST_DIR)
        )"""
