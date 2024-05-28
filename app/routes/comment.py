#!/usr/bin/python3

from flask import Blueprint, request, jsonify, redirect, url_for
from flask-login import login_required, current_user
from models import db, Comment, Post

comment_bp = Blueprint('comment', __name__)

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

