import os 

from flask import Flask

app = Flask(__name__)

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
