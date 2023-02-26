import datetime
from flask_login import UserMixin
from __init__ import db
from sqlalchemy import DateTime


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(1000), nullable=False)
    role = db.Column(db.String(1000), nullable=False)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100), nullable=False)


class event_scan(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)



class names(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    uid = db.Column(db.String(100), nullable=False)
    flag = db.Column(db.String(1), nullable=False, default=0)
