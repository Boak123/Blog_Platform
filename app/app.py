from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    db.init_app(app)
    login_manager.init_app(app)

    with app.app_context():
        from .routes import auth, post, comment, search, user
        app.register_blueprint(auth.bp)
        app.register_blueprint(post.bp)
        app.register_blueprint(comment.bp)
        app.register_blueprint(search.bp)
        app.register_blueprint(user.bp)

        db.create_all()
        
    return app
