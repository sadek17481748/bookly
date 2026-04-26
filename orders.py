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
