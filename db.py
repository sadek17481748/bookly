# Shared SQLAlchemy object — imported by models and blueprints so everything uses one metadata/session setup.

from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()
