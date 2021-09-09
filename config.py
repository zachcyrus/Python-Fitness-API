import os

if os.environ['LOCAL_DB_URI'] is None:
    os.environ['LOCAL_DB_URI'] = 'fakeurl'

class Config(object):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = 'fakeurl'

class DevelopmentConfig(Config):
    ENV = "development"
    DEVELOPMENT = True

class ProductionConfig(Config):
    ENV = "production"

class TestingConfig(Config):
    TESTING = True
    # Enter DB credentials later when it is implemented