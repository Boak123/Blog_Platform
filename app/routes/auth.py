#!/usr/bin/python3

from flask import Flask, request, jsonify, render_template, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import requests
from models import db, User, Post, comment, search


login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

auth_bp = Blueprint('auth', __name__)


""" Route to register user """
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        name = request.form.get('name')

        if not email or not password or not name:
            return jsonify({"error": "Missing email, password, or name"}), 400

        if User.query.filter_by(email=email).first():
            return jsonify({"error": "Email already exists"}), 400

        new_user = User(email=email, password=generate_password_hash(password, method='sha256'), name=name)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))

    return render_template('register.html')

                                                                                                                                   
""" Route to login user """
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if not user or not check_password_hash(user.password, password):
            return jsonify({"error": "Invalid email or password"}), 400

        login_user(user)
        return redirect(url_for('home'))

    return render_template('login.html')


""" Route to logout user """
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('landing_page'))
