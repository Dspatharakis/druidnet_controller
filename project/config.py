import os
from project import app

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    TESTING = False
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite://")
    REDIS_URL = "redis://redis:6379"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    app.config['MONGODB_SETTINGS'] = {
    'db': 'flaskdb',
    'host': 'mongodb',
    # 'username': 'flaskdbuser',
    # 'password': 'pass',
    'port': 27017
}



class DevelopmentConfig():
    TESTING = False
    WTF_CSRF_ENABLED = False


class TestingConfig():
    TESTING = True
    WTF_CSRF_ENABLED = False
    PRESERVE_CONTEXT_ON_EXCEPTION = False