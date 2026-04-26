from functools import wraps

from flask import Blueprint, abort, render_template
from flask_login import current_user, login_required
from sqlalchemy import desc, func

from db import db
from models import Book, Order, OrderItem, Review, User


admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


def admin_required(view_func):
    """
    Simple access control: user must be logged in AND is_admin.

    This keeps the dashboard private (normal users cannot access it).
    """

    @wraps(view_func)
    @login_required
    def wrapper(*args, **kwargs):
        if not getattr(current_user, "is_admin", False):
            abort(403)
        return view_func(*args, **kwargs)

    return wrapper

