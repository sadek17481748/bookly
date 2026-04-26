# Automated testing

Automated tests use **pytest** and Flask’s **test client**. They run against an **in-memory SQLite** database (`sqlite:///:memory:`) so you do **not** need PostgreSQL running to execute the suite.

## Run the tests

```bash
cd /path/to/bookly-final
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
pytest -v
```

Expected: **all tests pass** (green). For a one-line summary: `pytest -q`.

## What counts as “automated”

Each test is a Python function that **calls the real Flask app** and **asserts** on HTTP status codes and HTML content. That is machine-runnable regression testing—not a manual checklist alone.

## Feature → test mapping

| Feature / requirement | Test file | Test name | What is checked |
|----------------------|-----------|------------|------------------|
| Home page loads | `test_public_pages.py` | `test_home_ok` | `GET /` → 200, expected copy |
| Contact page | `test_public_pages.py` | `test_contact_ok` | `GET /contact` → 200 |
| Book catalog list | `test_public_pages.py` | `test_books_list_empty_ok` | `GET /books` → 200 |
| Book search query | `test_books_reviews.py` | `test_books_search_param_ok` | `?q=` returns matching book |
| Book detail | `test_public_pages.py` | `test_book_detail_ok` | `GET /books/<id>` shows title/author |
| Missing book | `test_public_pages.py` | `test_book_detail_404` | Unknown id → 404 |
| Static files | `test_public_pages.py` | `test_static_css_served` | `GET /static/css/styles.css` → 200 |
| Registration form | `test_auth.py` | `test_register_get_ok` | `GET /register` → 200 |
| Login form | `test_auth.py` | `test_login_get_ok` | `GET /login` → 200 |
| Register + login | `test_auth.py` | `test_register_login_flow` | New user can register, log out, log in |
| Register validation | `test_auth.py` | `test_register_password_mismatch` | Mismatch → redirect (error flash path) |
| Login validation | `test_auth.py` | `test_login_bad_password` | Wrong password → redirect to login |
| Review requires auth | `test_books_reviews.py` | `test_create_review_requires_login` | Guest POST review → redirect to login |
| Create review | `test_books_reviews.py` | `test_create_review_ok` | Logged-in user can post a review |
| Cart requires auth | `test_cart_orders_admin.py` | `test_cart_requires_login` | Guest `GET /cart` → redirect |
| Add to cart | `test_cart_orders_admin.py` | `test_add_to_cart_ok` | Logged-in user adds quantity |
| Checkout empty cart | `test_cart_orders_admin.py` | `test_checkout_empty_cart_redirects` | POST checkout with empty cart handled |
| Admin login gate | `test_cart_orders_admin.py` | `test_admin_analytics_requires_login` | Guest → redirect |
| Admin role | `test_cart_orders_admin.py` | `test_admin_analytics_forbidden_for_normal_user` | Non-admin → 403 |
| Admin dashboard | `test_cart_orders_admin.py` | `test_admin_analytics_ok_for_admin` | Admin user → 200, dashboard content |

## Limits (honest scope)

- **Payments** are not integrated; checkout tests cover empty-cart behaviour, not card gateways.
- **Email delivery** is not tested (there is no mailer).
- **Large UI** regressions are only covered where assertions inspect response HTML snippets.

Extend `tests/` with more functions as you add features; keep this table updated if your brief asks for explicit traceability.
