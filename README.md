# Workout Tracker API

## Purpose
Purpose of this project is to create an API that allows for workout tracking/keeping a log of workouts categorized in different routines, primarily using Python Flask.

## Technology
- Python
- Python Flask
- PostgreSQL
- Jenkins
- AWS

## Thought Process while building:
1. To first start creating this application I came up with a potential db schema. 
    ![Database schema](fitness-api-schema.png)

2. Next I searched for a python library to allow me to create tables and perform queries. This led me to [Python Flask SQL Alchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/)
Which is an extension of flask that allows for SQLAlchemy support thus allowing for object relational mapping with a SQL database. 

3. Thanks to SQLAlchemy it allows me to declare tables as Python classes, thus allowing me to create methods and functions to effectively manipulate my database, with the ease of Python.
    ```
    class User(db.Model):
        user_id = db.Column(db.Integer, primary_key=True)
        user_name = db.Column(db.String(50), unique=True, nullable=False)
        name = db.Column(db.String(50), nullable=False)
        email = db.Column(db.String(50), nullable=False)
        routines = db.relationship('User_Routines', backref='user', lazy=True)
        password = db.Column(db.String(100), nullable=False)


        def __init__(self,data):
            self.name = data.get('name')
            self.user_name = data.get('user_name')
            self.email = data.get('email')
            self.password = data.get('password')

        def __repr__(self):
            return '<User %r>' % self.name

        def save_to_db(self):
            db.session.add(self)
            db.session.commit()
            print('Saving to db')

        @staticmethod
        def select_all():
            user_query = User.query.all()
            response = []
            #returns an array of all User objects
            for user_obj in user_query:
                response.append({
                    'user_id':user_obj.user_id,
                    'user_name':user_obj.user_name,
                    'name':user_obj.name,
                    'email':user_obj.email
                })

            return response
    ```

4. Once my database tables are declared I begun working on the actual routes through with Python flask. 



## How to run
1. Add a .env file to the root of the directory with the following contents
    ```
    DEBUG=True
    FLASK_ENV=development
    FLASK_APP=api
    LOCAL_DB_URI=url to your pg db
    ```
2. Set up a python virtual environment in the root of the cloned repository.
```
$ python3 -m venv venv
$ . venv/bin/activate
$ pip install -r requirement.txt
```

3. Now in the terminal enter:
    ```
    $ flask run
    ```

## Features that still need to be added
- Recording completed workouts on different days 
- Implementing delete and update routes for routines and exercises
- Implement an AWS production database.