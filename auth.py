from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required, login_user, logout_user

from db import db
from models import User


auth_bp = Blueprint("auth", __name__)


@auth_bp.get("/register")
def register_form():
    return render_template("register.html")


@auth_bp.post("/register")
def register_submit():
    email = (request.form.get("email") or "").strip().lower()
    password = request.form.get("password") or ""
    password2 = request.form.get("password2") or ""

    if not email or not password:
        flash("Email and password are required.", "error")
        return redirect(url_for("auth.register_form"))

    if password != password2:
        flash("Passwords do not match.", "error")
        return redirect(url_for("auth.register_form"))

    if User.query.filter_by(email=email).first() is not None:
        flash("That email is already registered. Try logging in.", "error")
        return redirect(url_for("auth.login_form"))

    user = User(email=email)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    login_user(user)
    flash("Welcome! Your account was created.", "success")
    return redirect(url_for("books.list_books"))


@auth_bp.get("/login")
def login_form():
    return render_template("login.html")


@auth_bp.post("/login")
def login_submit():
    email = (request.form.get("email") or "").strip().lower()
    password = request.form.get("password") or ""

    user = User.query.filter_by(email=email).first()
    if user is None or not user.check_password(password):
        flash("Invalid email or password.", "error")
        return redirect(url_for("auth.login_form"))

    login_user(user)
    flash("You are now logged in.", "success")
    next_url = request.args.get("next")
    return redirect(next_url or url_for("books.list_books"))


@auth_bp.post("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged out.", "success")
    return redirect(url_for("home"))

