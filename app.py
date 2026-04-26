import os

from dotenv import load_dotenv
from flask import Flask, render_template
from flask_login import LoginManager

from cli import register_cli
from config import Config
from db import db
from models import User


def create_app() -> Flask:
    load_dotenv()  # reads .env locally (Heroku uses config vars)

    app = Flask(__name__)
    app.config.from_object(Config)

    if not app.config.get("SQLALCHEMY_DATABASE_URI"):
        raise RuntimeError(
            "DATABASE_URL is missing. Create a .env file (see .env.example)."
        )

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = "auth.login_form"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id: str):
        try:
            uid = int(user_id)
        except ValueError:
            return None
        return User.query.get(uid)

    # Blueprints
    from auth import auth_bp
    from admin import admin_bp
    from books import books_bp
    from cart import cart_bp
    from orders import orders_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(books_bp)
    app.register_blueprint(cart_bp)
    app.register_blueprint(orders_bp)
