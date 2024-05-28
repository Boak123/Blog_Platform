#!/usr/bin/python3

from flask import Blueprint, request, render_template, redirect, url_for
from flask_login import login_required, current_user
from models import db, Post

post_bp = Blueprint('post', __name__)

@posts_bp.route('/')
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
        return redirect(url_for('post.list_posts'))

    return render_template('create_post.html')

@post_bp.route('/post/<int:post_id>')
def view_post(post_id):
    post = Post.query.get_or_404(post_id)
    author = User.query.get(post.author_id)
    return render_template('view_post.html', post=post, author=author)
