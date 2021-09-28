from os import stat
import bcrypt
import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import backref
from bcrypt import hashpw, checkpw


from api import db


class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(50), unique=True, nullable=False)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    routines = db.relationship('User_Routines', backref='user', lazy=True)
    password = db.Column(db.String(128), nullable=False)


    def __init__(self,data):
        self.name = data.get('name')
        self.user_name = data.get('user_name')
        self.email = data.get('email')
        self.password = hashpw(data.get('password').encode('utf-8'), bcrypt.gensalt(16)).decode('utf8')

    def __repr__(self):
        return '<User %r>' % self.name

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
        print('Saving to db')

    def check_password(self, submitted_password):
        return checkpw(submitted_password.encode('utf-8'), self.password.encode('utf-8'))


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

    @staticmethod
    def find_username(username):
        found_user = User.query.filter_by(user_name=username).first()
        if found_user is None:
            return False
        else:
            return found_user

    @staticmethod
    def find_user_by_id(id):
        found_user = User.query.filter_by(user_id=id).first()
        if found_user is None:
            return False

        else:
            return found_user

    def delete_user(self):
        db.session.delete(self)
        db.session.commit()
        print('Deleting user with ID:',self.user_id)

    def get_routines(self):
        routines_list = self.routines

        print(routines_list)

        response = []

        for routine in routines_list:
            routine_row = Routines.find_routine_by_id(routine.routine_id)
            response.append({
                'routine_id':routine.routine_id,
                'routine_name':routine_row.routine_name,
                'routine_description':routine_row.routine_description
            })

        return response

    def find_routine(self,routine_name):
        routines_list = self.routines

        for routine in routines_list:
            routine_row = Routines.find_routine_by_id(routine.routine_id)

            if routine_row.routine_name == routine_name:
                return routine_row
        
        
        return False


class Routines(db.Model):
    routine_id = db.Column(db.Integer, primary_key=True)
    routine_name = db.Column(db.String(50), nullable=False)
    routine_description = db.Column(db.String(50), nullable=False)
    routines = db.relationship('User_Routines', cascade="all, delete-orphan", backref='routines', lazy=True)
    routine_exercises = db.relationship('Routine_Exercises', cascade="all, delete-orphan", backref='routines_exercises', lazy=True)

    def __init__(self,data):
        self.routine_name = data.get('routine_name')
        self.routine_description = data.get('routine_description')

    def save_routine(self):
        db.session.add(self)
        db.session.commit()
        print('Saving routine to db')


    def delete_routine(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def get_all_routines():
        all_routines = Routines.query.all()
        response_list = []
        for routine in all_routines:
            response_list.append({
                "routine_name": routine.routine_name,
                "routine_description": routine.routine_description
            })

        return response_list

    @staticmethod
    def find_routine_by_id(id):
        found_routine = Routines.query.filter_by(routine_id=id).first()

        if found_routine is None:
            return False

        else:
            return found_routine

    def get_exercises_in_routine(self):
        all_exercises = self.routine_exercises

        exercise_list = []

        for exercise in all_exercises:
            exercise_row = Exercises.find_exercise_by_id(exercise.exercise_id)
            exercise_list.append({
                "exercise_name": exercise_row.exercise_name,
                "exercise_description": exercise_row.exercise_description,
                "reps": exercise.reps

            })

        return exercise_list
        



    def __repr__(self):
        return f"{self.__class__.__name__} {self.routine_name}"

class Exercises(db.Model):
    exercise_id = db.Column(db.Integer, primary_key=True)
    exercise_name = db.Column(db.String(50), nullable=False)
    exercise_description = db.Column(db.String(50), nullable=False)
    routine_exercises = db.relationship('Routine_Exercises', backref='exercises_routine', lazy=True)


    def __init__(self,data):
        self.exercise_name = data.get("exercise_name")
        self.exercise_description = data.get("exercise_description")

    def save_exercise(self):
        db.session.add(self)
        db.session.commit()
        print('Saving exercise to db')

    @staticmethod
    def get_all_exercises():
        all_exercises = Exercises.query.all()
        response_list = []
        for exercise in all_exercises:
            response_list.append({
                "exercise_name": exercise.exercise_name,
                "exercise_description": exercise.exercise_description
            })

        return response_list

    @staticmethod
    def find_exercise_by_id(id):
        found_exercise = Exercises.query.filter_by(exercise_id=id).first()

        if found_exercise is None:
            return False

        else:
            return found_exercise


    def __repr__(self):
        return f"{self.__class__.__name__} {self.exercise_name}"

class User_Routines(db.Model):
    __tablename__ = 'user_routines'
    user_routine_id = db.Column(db.Integer(), primary_key=True)
    # relationship with routines and user tables
    user_id = db.Column(db.Integer(), db.ForeignKey('user.user_id'), nullable=False)
    routine_id = db.Column(db.Integer(), db.ForeignKey('routines.routine_id'), nullable=False)

    def save_user_routine(self):
        db.session.add(self)
        db.session.commit()
        print('Saving User Routines to db')

class Routine_Exercises(db.Model):
    __tablename__ = 'routine_exercises'
    routine_exercise_id = db.Column(db.Integer(), primary_key=True)
    reps = db.Column(db.Integer(), nullable=False)
    exercise_id = db.Column(db.Integer(), db.ForeignKey('exercises.exercise_id'), nullable=False)
    routine_id = db.Column(db.Integer(), db.ForeignKey('routines.routine_id'), nullable=False) 
    user_routine_exercises = db.relationship('User_Routine_Exercises', backref='exercises', lazy=True)

    def save_routine_exercises(self):
        db.session.add(self)
        db.session.commit()
        print('Saving Routine Exercises to db')

# This table is meant to show the exercises for a particular routine chosen by a user.
class User_Routine_Exercises(db.Model):
    __tablename__ = 'user_routine_exercises'
    personal_routine_exercise_id = db.Column(db.Integer(), primary_key=True)
    user_routine_id = db.Column(db.Integer(), db.ForeignKey('user_routines.user_routine_id'))
    routine_exercise_id = db.Column(db.Integer(), db.ForeignKey('routine_exercises.routine_exercise_id'))

    def save_user_routine_exercises(self):
        db.session.add(self)
        db.session.commit()
        print('Saving user routine exercises to db')

class Logs(db.Model):
    # Need determine best way to save date time
    log_id = db.Column(db.Integer, primary_key=True)
    date_completed = db.Column(db.DateTime(), default=datetime.datetime.now().isoformat())
    weight = db.Column(db.Float(), nullable=True)
    reps = db.Column(db.Integer(), nullable=False)
    personal_routine_id = db.Column(db.Integer(), db.ForeignKey('user_routine_exercises.personal_routine_exercise_id'))

    def save_logs(self):
        db.session.add(self)
        db.session.commit()
        print('Saving logs to database')