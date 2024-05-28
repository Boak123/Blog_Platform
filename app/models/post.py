#!/usr/bin/python3

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy

"""Post model"""
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140))
    content = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    comments = db.relationship('Comment', backref='post', lazy=True)
