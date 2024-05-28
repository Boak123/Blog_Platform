#!/usr/bin/python3

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy


"""search model"""
class Search(db.model):
    id = db.Column(db.Integer, primary_key=True)
    query = db.Column(db.String(150), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
