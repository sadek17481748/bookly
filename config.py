# Flask config: secrets and DB URL come from the environment (never hard-code real values here).

import os


class Config:
    # Session signing / CSRF (set a long random string in production)
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-only-change-me")
    # e.g. postgresql+psycopg2://user:pass@host:5432/dbname
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
