# ============================================================
# DATABASE MODELS (SQLAlchemy)
# - Table names match schema.sql
# - Money values are stored as integer cents (no floating point)
# - Relationships connect users ↔ reviews/cart/orders ↔ books
# ============================================================

from datetime import datetime

from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from db import db


# ================= USERS (LOGIN + CART + ORDERS) =================
class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)
