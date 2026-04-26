# bookly — Flask app factory, database, login, blueprints, and a few top-level routes.

import os

from dotenv import load_dotenv
from flask import Flask, render_template
from flask_login import LoginManager

from cli import register_cli
from config import Config
from db import db
from models import User


def create_app() -> Flask:
    # --- Environment & Flask config ---
    load_dotenv()  # loads .env in dev; production uses real environment variables

    app = Flask(__name__)
    app.config.from_object(Config)

    if not app.config.get("SQLALCHEMY_DATABASE_URI"):
        raise RuntimeError(
            "DATABASE_URL is missing. Create a .env file (see .env.example)."
        )

    # --- SQLAlchemy ---
    db.init_app(app)

    # --- Flask-Login (cookie session ↔ User row) ---
    login_manager = LoginManager()
    login_manager.login_view = "auth.login_form"  # where @login_required sends guests
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id: str):
        # Flask-Login calls this with the id stored in the session
        try:
            uid = int(user_id)
        except ValueError:
            return None
        return User.query.get(uid)

    # --- Blueprints: routes live in auth.py, books.py, cart.py, orders.py, admin.py ---
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

    # --- Pages not tied to a blueprint ---
    @app.get("/")
    def home():
        return render_template("home.html")

    @app.get("/contact")
    def contact():
        return render_template("contact.html")

    @app.errorhandler(403)
    def forbidden(_err):
        return render_template("403.html"), 403

    # --- Flask CLI: init-db, reset-db, make-admin ---
    register_cli(app)
    return app


# Used by `flask --app app` and by gunicorn (`app:app`)
app = create_app()


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "5000"))  # Heroku sets PORT
    app.run(host="0.0.0.0", port=port, debug=True)
