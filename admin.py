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


@admin_bp.get("/analytics")
@admin_required
def analytics_dashboard():
    total_users = db.session.query(func.count(User.id)).scalar() or 0
    total_reviews = db.session.query(func.count(Review.id)).scalar() or 0
    total_orders = db.session.query(func.count(Order.id)).scalar() or 0
    revenue_cents = db.session.query(func.coalesce(func.sum(Order.total_cents), 0)).scalar() or 0
    avg_order_cents = 0
    if total_orders > 0:
        avg_order_cents = int(revenue_cents / total_orders)

    recent_orders = (
        Order.query.order_by(Order.created_at.desc())
        .limit(10)
        .all()
    )

    # Top-selling books by quantity
    top_books = (
        db.session.query(
            Book.id,
            Book.title,
            Book.author,
            Book.category,
            func.coalesce(func.sum(OrderItem.quantity), 0).label("qty"),
            func.coalesce(func.sum(OrderItem.quantity * OrderItem.unit_price_cents), 0).label(
                "sales_cents"
            ),
        )
        .join(OrderItem, OrderItem.book_id == Book.id)
        .group_by(Book.id)
        .order_by(desc("qty"))
        .limit(10)
        .all()
    )

    # Basic inventory view: count of books by category
    books_by_category = (
        db.session.query(Book.category, func.count(Book.id).label("count"))
        .group_by(Book.category)
        .order_by(desc("count"))
        .all()
    )

    return render_template(
        "admin_analytics.html",
        total_users=total_users,
        total_reviews=total_reviews,
        total_orders=total_orders,
        revenue_cents=revenue_cents,
        avg_order_cents=avg_order_cents,
        recent_orders=recent_orders,
        top_books=top_books,
        books_by_category=books_by_category,
    )

