from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from api import db


class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(50))

    def __init__(self,data):
        self.name = data.get('name')
        self.user_id = data.get('id')
        self.email = 'fake@gmail.com'

    def __repr__(self):
        return '<User %r>' % self.name

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
        print('Saving to db')

    @staticmethod
    def select_all():
        response = User.query.all()
        return response