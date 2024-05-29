#!/usr/bin/python3

from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime


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


"""post model"""
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140))
    content = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    comments = db.relationship('Comment', backref='post', lazy=True)


"""Comment model"""
class Comment( db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


"""search model"""
class Search(db.model):
    id = db.Column(db.Integer, primary_key=True)
    query = db.Column(db.String(150), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
