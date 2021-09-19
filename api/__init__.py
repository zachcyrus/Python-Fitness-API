import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager


db = SQLAlchemy()
migrate = Migrate()

# Application factory
def create_app(testing=False):
    app = Flask(__name__)

    # Logic for handling configuration
    if app.config["ENV"] == 'production':
        app.config.from_object("config.ProductionConfig")

    elif app.config["ENV"] == 'testing':
        app.config.from_object("config.TestingConfig")

    else:
        app.config.from_object("config.DevelopmentConfig")

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    migrate.init_app(app,db)
    jwt = JWTManager(app)



    # importing api blueprint

    from api.api import api_bp
    app.register_blueprint(api_bp, url_prefix='/api')


    

    return app
