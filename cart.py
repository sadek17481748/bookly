from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from db import db
from models import Book, CartItem


cart_bp = Blueprint("cart", __name__, url_prefix="/cart")


def _cart_totals(items):
    subtotal_cents = 0
    for item in items:
        subtotal_cents += item.book.price_cents * item.quantity
    return subtotal_cents


@cart_bp.get("")
@login_required
def view_cart():
    items = (
        CartItem.query.filter_by(user_id=current_user.id)
        .join(Book, Book.id == CartItem.book_id)
        .all()
    )
    subtotal_cents = _cart_totals(items)
    return render_template("cart.html", items=items, subtotal_cents=subtotal_cents)
