import os 

from flask import Flask

app = Flask(__name__)

# Index route which will return Hello World.
@app.route('/')
def hello():
    return 'Hello, World!'
