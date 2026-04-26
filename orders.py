from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from db import db
from models import CartItem, Order, OrderItem


orders_bp = Blueprint("orders", __name__, url_prefix="/orders")


@orders_bp.get("")
@login_required
def list_orders():
    orders = (
        Order.query.filter_by(user_id=current_user.id)
        .order_by(Order.created_at.desc())
        .all()
    )
    return render_template("orders.html", orders=orders)


@orders_bp.get("/checkout")
@login_required
def checkout_form():
    items = CartItem.query.filter_by(user_id=current_user.id).all()
    subtotal_cents = sum(item.book.price_cents * item.quantity for item in items)
    return render_template("checkout.html", items=items, subtotal_cents=subtotal_cents)


@orders_bp.post("/checkout")
@login_required
def checkout_submit():
    """
    Simple checkout: creates an order based on current cart items.

    Notes:
    - We do not integrate real payments here.
    - We still store purchases in PostgreSQL as required.
    """

    items = CartItem.query.filter_by(user_id=current_user.id).all()
    if not items:
        flash("Your cart is empty.", "error")
        return redirect(url_for("cart.view_cart"))

    # Minimal form fields (beginner friendly)
    full_name = (request.form.get("full_name") or "").strip()
    address = (request.form.get("address") or "").strip()

    if not full_name or not address:
        flash("Name and address are required for checkout.", "error")
        return redirect(url_for("orders.checkout_form"))

    total_cents = sum(item.book.price_cents * item.quantity for item in items)
    order = Order(user_id=current_user.id, total_cents=total_cents)
    db.session.add(order)
    db.session.flush()  # ensures order.id is available

    for item in items:
        order_item = OrderItem(
            order_id=order.id,
            book_id=item.book_id,
            quantity=item.quantity,
            unit_price_cents=item.book.price_cents,
        )
        db.session.add(order_item)

    # Clear cart after successful "purchase"
    for item in items:
        db.session.delete(item)

    db.session.commit()
    flash("Purchase complete! Your order has been created.", "success")
    return redirect(url_for("orders.list_orders"))

