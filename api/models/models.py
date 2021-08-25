from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from api import db, user
import json


class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(50), unique=True, nullable=False)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)

    def __init__(self,data):
        self.name = data.get('name')
        self.user_name = data.get('user_name')
        self.email = data.get('email')

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

    @staticmethod
    def find_username(username):
        found_user = User.query.filter_by(user_name=username).first()
        if found_user is None:
            return False
        else:
            return True

