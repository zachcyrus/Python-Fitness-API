import os

class Config(object):
    DEBUG = False
    TESTING = False
    DATABSE_URI = os.environ['LOCAL_DB_URI']

class DevelopmentConfig(Config):
    ENV = "development"
    DEVELOPMENT = True

class ProductionConfig(Config):
    ENV = "production"

class TestingConfig(Config):
    TESTING = True
    # Enter DB credentials later when it is implemented