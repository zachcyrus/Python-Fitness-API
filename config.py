import os

if os.environ['LOCAL_DB_URI'] is None:
    os.environ['LOCAL_DB_URI'] = 'fakeurl'

class Config(object):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = os.environ['LOCAL_DB_URI']
    JWT_SECRET_KEY = os.environ['JWT_SECRET_KEY']

class DevelopmentConfig(Config):
    ENV = "development"
    DEVELOPMENT = True
    

class ProductionConfig(Config):
    ENV = "production"

class TestingConfig(Config):
    ENV = 'testing'
    TESTING = True
    # Enter DB credentials later when it is implemented
    SQLALCHEMY_DATABASE_URI = os.environ['TESTING_DB_URI']