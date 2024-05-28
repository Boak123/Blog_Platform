#!/usr/bin/python3

from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


db = SQLAlchemy


""" user model"""
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128)
    post = db.relationship('Post', backref='author', lazy=True)
    google_id = db.Column(db.String(150), unique=True, nullable=True)

    comments = db.relationship('Comment', backref='author', lazy=True)
    posts = db.relationship('Post', backref='author', lazy=True)
    searches = db.relationship('Search', backref='author', lazy=True)


    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
