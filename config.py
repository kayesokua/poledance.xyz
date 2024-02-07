from os import environ, path
from dotenv import load_dotenv
basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))

class Config():
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    UPLOAD_FOLDER = 'app/data/uploads/'
    FRAME_OUTPUT_FOLDER = 'app/data/processed/'
    SERVE_UPLOAD_FOLDER = 'data/uploads/'
    SERVE_PROCESSED_FOLDER = 'data/processed/'
    MODEL_PATH = 'app/extensions/models/pose_landmarker.task'
    pass
    
class TestingConfig(Config):
    SECRET_KEY = environ.get('SECRET_KEY_TEST')
    SQLALCHEMY_DATABASE_URI = environ.get('SQLALCHEMY_DATABASE_URI_TEST')
    DEBUG = False
    TESTING = True
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = False
    
class DevelopmentConfig(Config):
    SECRET_KEY = environ.get('SECRET_KEY_DEV')
    SQLALCHEMY_DATABASE_URI = environ.get('SQLALCHEMY_DATABASE_URI_DEV')
    DEBUG = True
    TESTING = True
    SQLALCHEMY_ECHO = False
    WTF_CSRF_ENABLED = True
    
class ProductionConfig(Config):
    SECRET_KEY = environ.get('SECRET_KEY_PROD')
    SQLALCHEMY_DATABASE_URI = environ.get('SQLALCHEMY_DATABASE_URI_PROD')
    DEBUG = False
    TESTING = False
    SQLALCHEMY_ECHO = True
    WTF_CSRF_ENABLED = True
