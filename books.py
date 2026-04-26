# Book catalog and reviews: list, detail, create/edit/delete (own reviews only).

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from db import db
from models import Book, Review


books_bp = Blueprint("books", __name__, url_prefix="/books")


# --- List & search (optional ?q= on title/author) ---
@books_bp.get("")
def list_books():
    q = (request.args.get("q") or "").strip()
    query = Book.query
    if q:
        like = f"%{q}%"
        query = query.filter((Book.title.ilike(like)) | (Book.author.ilike(like)))

    books = query.order_by(Book.created_at.desc()).all()
    return render_template("books.html", books=books, q=q)


# --- Single book + its reviews ---
@books_bp.get("/<int:book_id>")
def book_detail(book_id: int):
    book = Book.query.get_or_404(book_id)
    reviews = (
        Review.query.filter_by(book_id=book_id)
        .order_by(Review.created_at.desc())
        .all()
    )
    return render_template("book_detail.html", book=book, reviews=reviews)


# --- Create review (logged in only) ---
@books_bp.post("/<int:book_id>/reviews")
@login_required
def create_review(book_id: int):
    book = Book.query.get_or_404(book_id)
    rating_raw = request.form.get("rating") or ""
    body = (request.form.get("body") or "").strip()

    try:
        rating = int(rating_raw)
    except ValueError:
        rating = 0

    if rating < 1 or rating > 5:
        flash("Rating must be between 1 and 5.", "error")
        return redirect(url_for("books.book_detail", book_id=book.id))

    if not body:
        flash("Review text is required.", "error")
        return redirect(url_for("books.book_detail", book_id=book.id))

    review = Review(user_id=current_user.id, book_id=book.id, rating=rating, body=body)
    db.session.add(review)
    db.session.commit()

    flash("Review posted!", "success")
    return redirect(url_for("books.book_detail", book_id=book.id))


# --- Delete review (owner only) ---
@books_bp.post("/<int:book_id>/reviews/<int:review_id>/delete")
@login_required
def delete_review(book_id: int, review_id: int):
    review = Review.query.filter_by(id=review_id, book_id=book_id).first_or_404()

    if review.user_id != current_user.id:
        flash("You can only delete your own reviews.", "error")
        return redirect(url_for("books.book_detail", book_id=book_id))

    db.session.delete(review)
    db.session.commit()

    flash("Review deleted.", "success")
    return redirect(url_for("books.book_detail", book_id=book_id))


# --- Edit review (owner only): form + POST handler ---
@books_bp.get("/<int:book_id>/reviews/<int:review_id>/edit")
@login_required
def edit_review_form(book_id: int, review_id: int):
    review = Review.query.filter_by(id=review_id, book_id=book_id).first_or_404()

    if review.user_id != current_user.id:
        flash("You can only edit your own reviews.", "error")
        return redirect(url_for("books.book_detail", book_id=book_id))

    book = Book.query.get_or_404(book_id)
    return render_template("edit_review.html", book=book, review=review)


@books_bp.post("/<int:book_id>/reviews/<int:review_id>/edit")
@login_required
def edit_review_submit(book_id: int, review_id: int):
    review = Review.query.filter_by(id=review_id, book_id=book_id).first_or_404()

    if review.user_id != current_user.id:
        flash("You can only edit your own reviews.", "error")
        return redirect(url_for("books.book_detail", book_id=book_id))

    rating_raw = request.form.get("rating") or ""
    body = (request.form.get("body") or "").strip()

    try:
        rating = int(rating_raw)
    except ValueError:
        rating = 0

    if rating < 1 or rating > 5:
        flash("Rating must be between 1 and 5.", "error")
        return redirect(
            url_for("books.edit_review_form", book_id=book_id, review_id=review_id)
        )

    if not body:
        flash("Review text is required.", "error")
        return redirect(
            url_for("books.edit_review_form", book_id=book_id, review_id=review_id)
        )

    review.rating = rating
    review.body = body
    db.session.commit()

    flash("Review updated.", "success")
    return redirect(url_for("books.book_detail", book_id=book_id))
