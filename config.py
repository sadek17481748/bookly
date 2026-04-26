# ============================================================
# FLASK CONFIGURATION
# - Reads secrets and database URL from environment variables
# - Avoids hard-coding real credentials in source control
# ============================================================

import os


class Config:
    # ================= SESSION / SECURITY =================
    # Session signing / CSRF (use a long random string in production).
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-only-change-me")
    # ================= DATABASE URL =================
    # Example: postgresql+psycopg2://user:pass@host:5432/dbname
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    # ================= SQLALCHEMY SETTINGS =================
    SQLALCHEMY_TRACK_MODIFICATIONS = False
