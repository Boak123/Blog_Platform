#!/usr/bin/python3

from flask import Blueprint, render_template
from flask_login import login_required, current_user
from models import User, Post

user_bp = Blueprint('user', __name__)

@user_bp.route('/dashboard')
@login_required
def dashboard():
    user = User.query.get(current_user.id)
    posts = BlogPost.query.filter_by(author_id=user.id).all()
    return render_template('dashboard.html', user=user, posts=posts)

@user_bp.route('/profile')
@login_required
def profile():
    user = User.query.get(current_user.id)
    return render_template('profile.html', user=user)

