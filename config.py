from os import environ, path
from dotenv import load_dotenv
basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))

class Config():
    SECRET_KEY = environ.get('SECRET_KEY_DEV')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    pass
    
class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = environ.get('SQLALCHEMY_DATABASE_URI_DEV')
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = True
    UPLOAD_FOLDER = 'app/data/uploads/'
    FRAME_OUTPUT_FOLDER = 'app/data/processed/'
    SERVE_UPLOAD_FOLDER = 'data/uploads/'
    SERVE_PROCESSED_FOLDER = 'data/processed/'
    MODEL_PATH = 'app/extensions/models/pose_landmarker.task'

class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = environ.get('SQLALCHEMY_DATABASE_URI_TEST')
    UPLOAD_FOLDER = 'app/data/uploads/'
    FRAME_OUTPUT_FOLDER = 'app/data/processed/'
    MODEL_PATH = 'app/extensions/models/pose_landmarker.task'