import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

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


    # Index route which will return Hello World.
    @app.route('/')
    def hello():
        return 'Hello, World!'

    # Importing modules
    from . import user
    from .routes import exercises

    # Registering blueprint routes
    app.register_blueprint(user.bp)
    app.register_blueprint(exercises.bp)

    return app
