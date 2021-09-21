import os

class Config(object):
    DEBUG = False
    TESTING = False
    JWT_SECRET_KEY = os.environ['JWT_SECRET_KEY'] or 'null'

class DevelopmentConfig(Config):
    ENV = "development"
    DEVELOPMENT = True
    SQLALCHEMY_DATABASE_URI = os.getenv('LOCAL_DB_URI') or 'null'
    

class ProductionConfig(Config):
    ENV = "production"

class TestingConfig(Config):
    ENV = 'testing'
    TESTING = True
    # Enter DB credentials later when it is implemented
    SQLALCHEMY_DATABASE_URI = os.environ['TESTING_DB_URI'] or 'null'
    