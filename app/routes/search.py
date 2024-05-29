#!/usr/bin/python3

from flask import Blueprint, request, render_template
from models import Post

search_bp = Blueprint('search', __name__)

@search_bp.route('/search')
def search():
    query = request.args.get('q')
    if query:
        results = Post.query.filter(Post.title.contains(query) | Post.content.contains(query)).all()
    else:
        results = []
    return render_template('search_results.html', results=results, query=query)
