# Shopping cart: list lines, add book, change quantity, remove line (per logged-in user).

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from db import db
from models import Book, CartItem


cart_bp = Blueprint("cart", __name__, url_prefix="/cart")


def _cart_totals(items):
    # Sum line totals in cents (expects each item.book loaded)
    subtotal_cents = 0
    for item in items:
        subtotal_cents += item.book.price_cents * item.quantity
    return subtotal_cents


# --- Cart page ---
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


# --- Add (merges quantity if same book already in cart — unique user+book in DB) ---
@cart_bp.post("/add/<int:book_id>")
@login_required
def add_to_cart(book_id: int):
    book = Book.query.get_or_404(book_id)
    qty_raw = request.form.get("quantity") or "1"

    try:
        qty = int(qty_raw)
    except ValueError:
        qty = 1

    if qty < 1:
        qty = 1

    item = CartItem.query.filter_by(user_id=current_user.id, book_id=book.id).first()
    if item is None:
        item = CartItem(user_id=current_user.id, book_id=book.id, quantity=qty)
        db.session.add(item)
    else:
        item.quantity += qty

    db.session.commit()
    flash(f"Added to cart: {book.title}", "success")
    return redirect(url_for("cart.view_cart"))


# --- Quantity update (0 or below removes the row) ---
@cart_bp.post("/update/<int:item_id>")
@login_required
def update_quantity(item_id: int):
    item = CartItem.query.filter_by(id=item_id, user_id=current_user.id).first_or_404()
    qty_raw = request.form.get("quantity") or "1"

    try:
        qty = int(qty_raw)
    except ValueError:
        qty = 1

    if qty < 1:
        db.session.delete(item)
    else:
        item.quantity = qty

    db.session.commit()
    flash("Cart updated.", "success")
    return redirect(url_for("cart.view_cart"))


# --- Remove one line ---
@cart_bp.post("/remove/<int:item_id>")
@login_required
def remove_item(item_id: int):
    item = CartItem.query.filter_by(id=item_id, user_id=current_user.id).first_or_404()
    db.session.delete(item)
    db.session.commit()
    flash("Removed from cart.", "success")
    return redirect(url_for("cart.view_cart"))
