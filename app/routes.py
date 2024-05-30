#!/usr/bin/python3

from flask import Flask, Blueprint, request, jsonify, render_template, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import requests
from models import db, User, Post, Comment, Search


login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

auth_bp = Blueprint('auth', __name__)
user_bp = Blueprint('user', __name__)
post_bp = Blueprint('post', __name__)
comment_bp = Blueprint('comment', __name__)
search_bp = Blueprint('search', __name__)



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
        return redirect(url_for('auth.login'))

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
    return redirect(url_for('auth.login'))


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


@post_bp.route('/')
def home():
    posts = Post.query.all()
    return render_template('posts/home.html', posts=posts)

@post_bp.route('/posts/<int:post_id>')
def list_posts(post_id):
    posts = Post.query.get_or_404(post_id)
    return render_template('home.html', posts=posts)

@post_bp.route('/post/create', methods=['GET', 'POST'])
@login_required
def create_post():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')

        if not title or not content:
            return jsonify({"error": "Missing title or content"}), 400

        new_post = Post(title=title, content=content, author_id=current_user.id)
        db.session.add(new_post)
        flash('Post created successfully!', 'success')
        db.session.commit()
        return redirect(url_for('post.home'))

    return render_template('create_post.html')

@post_bp.route('/post/<int:post_id>')
def view_post(post_id):
    post = Post.query.get_or_404(post_id)
    author = User.query.get(post.author_id)
    return render_template('view_post.html', post=post, author=author)


@comment_bp.route('/post/<int:post_id>/comment', methods=['POST'])
@login_required
def add_comment(post_id):
    content = request.form.get('content')

    if not content:
        return jsonify({"error": "Missing content"}), 400

    post = Post.query.get_or_404(post_id)

    new_comment = Comment(content=content, author_id=current_user.id, post_id=post.id)
    db.session.add(new_comment)
    db.session.commit()

    return redirect(url_for('post.view_post', post_id=post.id))


@search_bp.route('/search')
def search():
    query = request.args.get('q')
    if query:
        results = Post.query.filter(Post.title.contains(query) | Post.content.contains(query)).all()
    else:
        results = []
    return render_template('search_results.html', results=results, query=query)
