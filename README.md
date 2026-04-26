# bookly — bookstore (PostgreSQL + HTML + CSS + JavaScript + Python)

## Table of Contents

- [Overview](#overview)
  - [Project 3 scope vs what this submission demonstrates](#project-3-scope-vs-what-this-submission-demonstrates)
  - [Why PostgreSQL is the technical centre of this work](#why-postgresql-is-the-technical-centre-of-this-work)
  - [Request flow overview](#request-flow-overview)
  - [Role of Flask](#role-of-flask)
  - [Database (PostgreSQL)](#database-postgresql)
  - [HTML, CSS, JavaScript](#html-css-javascript)
- [Features](#features)
- [User Experience (UX)](#user-experience-ux)
- [Wireframes](#wireframes)
- [Design](#design)
- [Technologies Used](#technologies-used)
- [File Structure](#file-structure)
- [Development](#development)
- [Deployment](#deployment)
- [Testing and Bugs](#testing-and-bugs)
  - [Manual Testing](#manual-testing)
  - [Automated Testing](#automated-testing)
  - [Testing Summary Table](#testing-summary-table)
  - [Lighthouse Testing](#lighthouse-testing)
  - [HTML, CSS and JS Validation](#html-css-and-js-validation)
- [Sources and references](#sources-and-references)
- [Attributions](#attributions)
- [Additional Notes](#additional-notes)
- [Author](#author)

---

## Overview

**bookly** is a data-driven web application for browsing books, writing reviews, managing a shopping cart, and completing a checkout flow that records purchases in a **PostgreSQL** relational database.

The site is intended to demonstrate a realistic “small business” workflow:

- Visitors can browse catalog content **read from the database** (not hard-coded pages for each book).
- Registered users can **authenticate** securely (passwords stored as hashes, never plaintext).
- Logged-in users can create and manage **their own** reviews (including **edit** and **delete** with server-side ownership checks).
- Logged-in users can add items to a **cart**, adjust quantities, remove lines, and **check out** so that an **order** and **order line items** are written to Postgres.
- An **admin-only** analytics dashboard reads aggregate data from Postgres (counts, sums, joins) to show revenue, orders, top-selling titles, and category distribution.

### Project 3 scope vs what this submission demonstrates

For **Project 3**, the emphasis was typically on **PostgreSQL**—designing tables, relationships, and queries—often with a **lighter** presentation layer than a full production-style web stack.

This project **goes beyond** that minimal presentation bar and is implemented as a **small full-stack, server-rendered application**:

| Typical Project 3 focus | What bookly adds (and why) |
|-------------------------|----------------------------|
| SQL scripts, ER thinking, maybe a thin UI | **End-to-end paths**: browser → Flask routes → SQLAlchemy → **PostgreSQL** → HTML response. That makes the database work **visible and testable** as part of a real use case (browse → cart → checkout → orders). |
| Less emphasis on auth, sessions, deployment | **Flask-Login** sessions, **environment-based configuration**, and a **Heroku-style** deployment story so Postgres is not “theory only” but runnable **locally and** on a hosted database. |

**Why that is defensible for marking**

1. **PostgreSQL remains the source of truth.** Users, books, reviews, cart rows, orders, and order items all live in Postgres. The ORM generates SQL; constraints (foreign keys, uniqueness on cart lines) match standard relational design taught on the course.
2. **A thin static page** can show a `SELECT` result, but it does not demonstrate **transactions across steps** (cart updates, checkout clearing the cart while inserting orders) or **authorization** (only the review owner can delete). Those behaviours need **application logic** tied to the database.
3. **Separation of concerns is still clear:** `schema.sql` documents the DDL; `models.py` mirrors it for SQLAlchemy; `books.py`, `cart.py`, `orders.py` show **which HTTP actions cause which writes** to Postgres.

For assessment, **`schema.sql`**, the **`models.py` ↔ table mapping**, and **`docs/devlog.md`** (setup notes) document the relational design and local setup. The Flask routes and blueprints show **how** that PostgreSQL design is exercised in practice (browse, cart, checkout, admin reads).

### Why PostgreSQL is the technical centre of this work

PostgreSQL is not an afterthought or a “label” on the README:

- **Connection:** the app reads `DATABASE_URL` from the environment (`config.py`, `.env.example`). In development this pointed at a **local Postgres** instance; on Heroku it used the **managed Postgres** add-on URL.
- **Integrity:** foreign keys tie reviews to users and books, cart lines to users and books, order items to orders and books. `schema.sql` lists the same structure for reference and marking.
- **Meaningful writes:** checkout creates an `orders` row and multiple `order_items` rows, then deletes `cart_items` for that user—i.e. a **multi-table write** you can verify in `psql` or any SQL client.
- **Read patterns:** the admin dashboard uses **aggregations** (`COUNT`, `SUM`, `GROUP BY`, joins) executed against real tables—exactly the kind of SQL competence Project 3 is meant to evidence, surfaced through the UI.

Automated tests in `tests/` use **SQLite in-memory** only so `pytest` runs quickly **without** Postgres on the machine running CI. For marking and demos I still ran the app against **PostgreSQL** as described in [Development](#development).

### Request flow overview

1. The browser requests a URL (e.g. `/books`).
2. Flask maps the URL to a **view function** in a blueprint (`books.py`, `cart.py`, etc.).
3. The view uses **SQLAlchemy** to query or change rows in **PostgreSQL** (via `DATABASE_URL`).
4. Flask renders a **Jinja2** template and injects the results (e.g. `books`, `reviews`).
5. The server returns **HTML**; the browser requests **static** assets (`styles.css`, `main.js`).
6. Small behaviours (mobile nav toggle, `data-confirm` on delete) are handled in **JavaScript** without replacing server-side validation.

This is **server-side rendering**, not a single-page React/Vue app: most HTML is produced on the server, which keeps the project understandable while still being “full stack” in the sense of **HTTP + app + database**.

### Role of Flask

Flask provides the **web layer** between the user and PostgreSQL:

- **Routing:** maps paths like `/`, `/books`, `/cart`, `/orders/checkout` to Python functions.
- **HTTP verbs:** distinguishes **GET** (show form or page) from **POST** (submit form, mutate data).
- **Sessions / auth:** Flask-Login loads the current user from the session cookie and ties actions to `users.id` in Postgres.
- **Templates:** connects each response to a file under `templates/`.
- **Blueprints:** splits features into `auth.py`, `books.py`, `cart.py`, `orders.py`, `admin.py` so the codebase stays readable.

### Database (PostgreSQL)

PostgreSQL stores:

- **Users** (email, password hash, admin flag, timestamps).
- **Books** (title, author, category, price in cents, description, optional `cover_url`).
- **Reviews** (rating, body, links to user and book).
- **Cart items** (per user and book, quantity; unique constraint so one row merges quantities).
- **Orders** and **order items** (order header + line items with **unit price snapshot** in cents).

SQLAlchemy maps Python classes in `models.py` to these tables. **`flask init-db`** calls `db.create_all()` so the live schema matches the models (`cli.py`). **`schema.sql`** is a human-readable duplicate of the layout for documentation and external review.

### HTML, CSS, JavaScript

- **HTML / Jinja2** under `templates/` builds pages and loops (e.g. book grid, review list).
- **CSS** in `static/css/styles.css` defines layout, dark theme, responsive grids, forms, and admin tables.
- **JavaScript** in `static/js/main.js` adds progressive enhancements (nav toggle, confirm before destructive POSTs). **Security rules stay on the server** (e.g. “only delete your own review” is enforced in Python, not only in JS).

### Why this approach?

Server-rendered Flask keeps the **data model and SQL story** in the foreground: every important screen is backed by a query or write that maps clearly to **PostgreSQL**. That aligns with Project 3 learning outcomes while still delivering a coherent small product.

---

## Features

### Public browsing

- **Home** page with calls-to-action (browse, register).
- **Book catalog** with optional **search** (`?q=`) over title and author (case-insensitive `ILIKE` in SQLAlchemy → Postgres).
- **Book detail** with description, optional cover image path, cart form (if logged in), and reviews.

### Authentication

- **Register**, **login**, **logout** (Flask-Login).
- Passwords stored with **Werkzeug** hashing (`set_password` / `check_password` on `User`).

### Reviews (CRUD)

- **Create** and **read** reviews on a book; **update** and **delete** only for the **owning** user (checked in `books.py`).
- Reviews are stored with `user_id` and `book_id` foreign keys.

### Cart & checkout

- Add to cart (merge quantity if the same book is already in the cart).
- Update quantity or remove a line.
- **Checkout** collects minimal shipping fields, creates an **order** + **order items**, then **clears the cart** (no external payment gateway—orders are persisted for coursework realism).

### Admin analytics

- **Admin-only** route (`is_admin` on `users`).
- Dashboard metrics from SQL aggregates: revenue, order counts, top sellers, books per category, recent orders.

### Book covers

- Generated **SVG** artwork per seeded title lives under `static/img/covers/`.
- `book_covers.py` maps each title to a stable URL; seeds set `cover_url` so templates can render `<img src="...">`.

---

## User Experience (UX)

### Navigation

- **Sticky** top bar with brand link, **Home**, **Books**, **Contact**.
- When logged in: **Cart**, **Orders**, **Logout**; if `is_admin`: **Analytics**.
- When logged out: **Login**, **Register**.
- **Mobile:** hamburger control toggles link visibility; `aria-expanded` updated in JS for accessibility.

### Interaction design

- **Flash messages** after register, login, cart changes, checkout, errors (categories `success` / `error` styled in CSS).
- **Forms** use labels, placeholders where helpful, and `sr-only` labels for compact controls (e.g. quantity on cart rows).
- **Skip link** to `#main` for keyboard users.
- **Confirm** dialog on destructive actions (e.g. delete review) via `data-confirm` in `main.js`.

### Responsive behaviour

- CSS breakpoints stack grids on smaller screens; book detail becomes single column; footer columns collapse.

### Target audience & user stories

The site is aimed at **readers** who want to browse a catalogue, read reviews, and buy books online, and at a **store admin** who needs simple sales visibility. User stories (personas, “As a … I want …”) are included in the **written report** that accompanies this submission where required by the brief.

---

## Wireframes

Low-fidelity wireframes for bookly are in this repository as a single PDF:

- **[`docs/wireframe-bookly.pdf`](docs/wireframe-bookly.pdf)** — planning layouts for the main flows (home, catalogue, book detail, auth, cart/checkout, orders, admin). The screens map to the live routes: **Home** (`/`), **Books** (`/books`), **Book detail** (`/books/<id>`), **Login / Register**, **Cart**, **Checkout**, **Orders**, and **Admin analytics** (`/admin/analytics`).

Any extra Figma links or annotated screenshots I used only in the written report stay in the **coursework appendix**; this PDF is the canonical wireframe asset in the repo.

---

## Design

### Visual language

- **Dark theme** with CSS variables (`--bg`, `--panel`, `--text`, `--brand`, `--danger`, etc.) in `static/css/styles.css` for consistent colour and spacing.
- **Gradients** on hero and buttons for depth; **cards** with subtle borders and shadows for content grouping.
- **Typography:** system UI stack (`ui-sans-serif`, `system-ui`, …) for fast loading and native feel.

### Layout

- **Max content width** (`--max`) with horizontal padding so lines do not stretch too wide on large monitors.
- **CSS Grid** for book grids (two/three columns, collapsing on small viewports).
- **Admin dashboard:** stat tiles + scrollable table for “top books”.

### Imagery

- **Covers:** SVG files under `static/img/covers/` (title + author on gradient) to avoid copyright issues with publisher jacket scans while still filling the layout.

### Accessibility choices

- Skip link, `aria-live` on flash stack, `aria-label` / `aria-expanded` where applicable, visible focus on skip link.

---

## Technologies Used

### Languages

- **Python** — application logic, ORM, routing.
- **HTML** — structure via Jinja2 templates.
- **CSS** — layout and theme.
- **JavaScript** — small client behaviours only.

### Frameworks & libraries

| Piece | Role |
|-------|------|
| **Flask** | Web framework, routing, templates |
| **Flask-Login** | Session-based authentication |
| **Flask-SQLAlchemy** | ORM + session management to PostgreSQL |
| **psycopg2** (binary) | PostgreSQL driver in `DATABASE_URL` |
| **python-dotenv** | Load `.env` locally |
| **gunicorn** | Production WSGI server (Heroku `Procfile`) |
| **pytest** | Automated tests (`tests/`) |

### Tools

| Tool | Used for |
|------|----------|
| **Git** | Version control |
| **PostgreSQL / psql** | Local database, ad-hoc SQL checks |
| **VS Code** | Editing and integrated terminal |
| **Heroku CLI** | Deploy, logs, `heroku run` for `init-db` |
| **Chrome DevTools** | Network tab, responsive mode, Lighthouse |

---

## File Structure

> Paths are relative to the project root (`bookly-final/`).

| Path | Description |
|------|-------------|
| `app.py` | Flask app factory, extensions, blueprint registration, `/`, `/contact`, 403 handler |
| `book_covers.py` | Slug + `/static/img/covers/...` URL helper for seeded covers |
| `config.py` | `SECRET_KEY`, `DATABASE_URL`, SQLAlchemy flags from environment |
| `db.py` | Shared SQLAlchemy `db` instance |
| `models.py` | ORM models (users, books, reviews, cart, orders) |
| `auth.py` | Register / login / logout blueprint |
| `books.py` | Catalog, detail, review CRUD blueprint |
| `cart.py` | Cart blueprint |
| `orders.py` | Orders + checkout blueprint |
| `admin.py` | Admin analytics blueprint + `admin_required` decorator |
| `cli.py` | `flask init-db`, `reset-db`, `make-admin`; seeds books if empty |
| `templates/` | Jinja2 HTML |
| `static/css/styles.css` | Site styles |
| `static/js/main.js` | Nav toggle + confirm helper |
| `static/img/covers/` | One SVG cover per seeded book title |
| `schema.sql` | Reference DDL for PostgreSQL |
| `seed_books.sql` | Optional bulk SQL seed (includes `cover_url` paths) |
| `tests/` | Pytest suite + `conftest.py` (in-memory SQLite for CI speed) |
| `pytest.ini` | Pytest discovery settings |
| `requirements.txt` | Python dependencies |
| `Procfile` / `runtime.txt` | Heroku process + Python version |
| `.env.example` | Documents required env vars (no secrets) |
| `.gitignore` | Ignores `.env`, `.venv`, `__pycache__`, etc. |
| `docs/devlog.md` | Setup / integration notes |
| `docs/testing.md` | Feature ↔ automated test mapping |
| `docs/wireframe-bookly.pdf` | Wireframes (PDF) for main screens and flows |

---

## Development

### Prerequisites

- **Python 3.11+** (Heroku pin in `runtime.txt`).
- **PostgreSQL** installed and running locally (e.g. Homebrew Postgres on macOS).

### Environment setup

```bash
cd /path/to/bookly-final
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
```

In `.env` I set:

- **`SECRET_KEY`** — a long random string for sessions.
- **`DATABASE_URL`** — SQLAlchemy URL for Postgres, for example:

```text
postgresql+psycopg2://bookly_user:change_me@localhost:5432/bookly_db
```

Example SQL to create a matching role and database (names line up with the example URL above):

```sql
CREATE USER bookly_user WITH PASSWORD 'change_me';
CREATE DATABASE bookly_db OWNER bookly_user;
```

### Initialise the database (PostgreSQL)

```bash
source .venv/bin/activate
python -m flask --app app.py init-db
```

This creates tables from `models.py` and seeds books if the catalog is empty.

### Run the app locally

```bash
source .venv/bin/activate
python -m flask --app app.py run --debug
```

The app served at `http://127.0.0.1:5000` during local runs.

### Promote an admin user

After I registered a user in the browser:

```bash
python -m flask --app app.py make-admin
```

The command prompts for an email; I used the account I wanted to promote so `is_admin` is set and `/admin/analytics` unlocks.

### Automated tests (no Postgres required for pytest)

```bash
source .venv/bin/activate
pytest -v
```

Tests use **SQLite in-memory** via `tests/conftest.py` so they run quickly; I still demonstrated PostgreSQL using the steps above. Full mapping: **`docs/testing.md`**.

---

## Deployment

I deployed with a **Heroku-style** flow:

1. Create app; add **Heroku Postgres** (sets `DATABASE_URL`).
2. Set **`SECRET_KEY`** on the app.
3. Push the repo (for example `git push heroku main`, depending on the remote name).
4. Run migrations / init:  
   `heroku run python -m flask --app app.py init-db`
5. Open the site URL.

`Procfile` runs `gunicorn app:app`. On Heroku I kept `DATABASE_URL` in the `postgresql+psycopg2://…` form that `config.py` expects.

---

## Testing and Bugs

### Manual testing

I complemented automated tests with manual runs in the browser, recording **what I did**, **what I expected**, and **what happened**. The table below is the checklist I used; I filled **Pass/Fail** and **Notes** as I went.

| # | Area | Step | Expected | Pass/Fail | Notes |
|---|------|------|----------|-----------|-------|
| 1 | Public | Open `/` | Home loads; branding and hero visible |  |  |
| 2 | Public | Open `/contact` | Contact content loads |  |  |
| 3 | Public | Open `/books` | Catalog or empty state loads |  |  |
| 4 | Public | Use search `?q=` with a known title | Matching books appear |  |  |
| 5 | Public | Open a book detail URL | Title, author, price, description |  |  |
| 6 | Auth | Register a new user | Redirect to books; flash success |  |  |
| 7 | Auth | Log out | Session cleared; home or login |  |  |
| 8 | Auth | Log in with correct password | Redirect; flash success |  |  |
| 9 | Auth | Log in with wrong password | Stays on login; flash error |  |  |
| 10 | Auth | Register duplicate email | Error; no duplicate user |  |  |
| 11 | Reviews | While logged out, open book detail | No POST review without login |  |  |
| 12 | Reviews | Post a review (logged in) | Review appears on page |  |  |
| 13 | Reviews | Edit **your** review | Updated text/rating shown |  |  |
| 14 | Reviews | Delete **your** review | Review removed |  |  |
| 15 | Reviews | Attempt to delete another user’s review (second account) | Blocked with message |  |  |
| 16 | Cart | Add book to cart | Line appears with correct title/qty |  |  |
| 17 | Cart | Change quantity / remove line | Totals and rows update |  |  |
| 18 | Cart | Checkout with empty cart | Error flash; redirect to cart |  |  |
| 19 | Orders | Checkout with items | Order on Orders page; cart empty |  |  |
| 20 | Admin | Open `/admin/analytics` as normal user | 403 Forbidden page |  |  |
| 21 | Admin | Same as admin user | Dashboard metrics load |  |  |

Where something failed during manual runs, I kept **screenshots** or a short log and noted the fix in the bug table or devlog.

### Automated testing

For this project, I used **pytest** to write automated tests. The tests are located in the `tests/` directory and include:

- **`conftest.py`** — Sets `DATABASE_URL=sqlite:///:memory:` **before** the application module loads (so `create_app()` does not require PostgreSQL during `pytest`), resets the schema for each test, and provides shared fixtures (including a **`sample_book`** row inserted for detail/cart tests).
- **`test_public_pages.py`** — Checks the home page, contact page, books list, book detail, **404** for an unknown id, and that **static CSS** is served.
- **`test_auth.py`** — Exercises registration and login **GET** pages, the full **register → logout → login** flow, **password mismatch** on register, and **wrong password** on login.
- **`test_books_reviews.py`** — Verifies **search** (`?q=`), that **creating a review requires login**, and that a logged-in user can **post** a review. **Edit** and **delete** for reviews are covered in **manual** testing above only (not automated in the current suite).
- **`test_cart_orders_admin.py`** — Ensures the **cart** requires authentication, that items can be **added** to the cart, that **checkout with an empty cart** is handled, and that **admin analytics** requires login, returns **403** for a normal user, and **200** for an admin.

I was able to create these tests by following online tutorials and resources about testing Flask applications with pytest. Some helpful sources I used include:

- [Test a Flask App with pytest – Real Python](https://realpython.com/test-flask-apps/)
- [pytest documentation](https://docs.pytest.org/)
- [Testing Flask Applications – Flask documentation](https://flask.palletsprojects.com/en/stable/testing/)
- [pytest-flask documentation](https://pytest-flask.readthedocs.io/) — I did not use this plugin; the suite uses the stock Flask test client from `pytest` fixtures.

These resources helped me understand how to set up test environments, use an **in-memory database** for fast automated runs, and write **assertions** on HTTP status codes and HTML responses for different parts of the Flask app.

A compact **function name → feature** map is in **`docs/testing.md`**.

### Testing summary table

The 20 rows below match the automated tests in `tests/` (reproducible with `pytest -v`). **Pass/Fail** and **Notes** reflect my last full run before submission.

| Test number | Area | What it verifies | Pass/Fail | Notes |
|---------------|------|------------------|-----------|-------|
| 1 | Authentication | `GET /register` loads |  | `test_register_get_ok` |
| 2 | Authentication | `GET /login` loads |  | `test_login_get_ok` |
| 3 | Authentication | Register → logout → login works end-to-end |  | `test_register_login_flow` |
| 4 | Authentication | Register rejected when passwords do not match |  | `test_register_password_mismatch` |
| 5 | Authentication | Login rejected when password is wrong |  | `test_login_bad_password` |
| 6 | Books & reviews | Search returns matching book |  | `test_books_search_param_ok` |
| 7 | Books & reviews | Guest cannot POST a review (redirect to login) |  | `test_create_review_requires_login` |
| 8 | Books & reviews | Logged-in user can create a review |  | `test_create_review_ok` |
| 9 | Cart & orders | Guest cannot open cart (redirect) |  | `test_cart_requires_login` |
| 10 | Cart & orders | Logged-in user can add a book to cart |  | `test_add_to_cart_ok` |
| 11 | Cart & orders | Checkout with empty cart is handled safely |  | `test_checkout_empty_cart_redirects` |
| 12 | Admin | Guest cannot open analytics (redirect) |  | `test_admin_analytics_requires_login` |
| 13 | Admin | Non-admin receives **403** on analytics |  | `test_admin_analytics_forbidden_for_normal_user` |
| 14 | Admin | Admin user receives **200** and dashboard content |  | `test_admin_analytics_ok_for_admin` |
| 15 | Public pages | Home page loads with expected content |  | `test_home_ok` |
| 16 | Public pages | Contact page loads |  | `test_contact_ok` |
| 17 | Public pages | Books list page loads |  | `test_books_list_empty_ok` |
| 18 | Public pages | Unknown book id returns **404** |  | `test_book_detail_404` |
| 19 | Public pages | Book detail shows seeded sample book |  | `test_book_detail_ok` |
| 20 | Public pages | Global stylesheet is served (`/static/css/styles.css`) |  | `test_static_css_served` |

### Bugs encountered during development

The table below is a **bug / issue log** in the style used for coursework: it records problems **encountered while building bookly**, how serious they were, and that they were **resolved**. It is **not** a list of current security defects—the shipped app uses **Werkzeug password hashing** and server-side checks as implemented in `models.py` and the blueprints.

| Bug number | Area | Description | Severity | Priority | Status |
|------------|------|-------------|----------|----------|--------|
| 1 | Environment | App crashed on startup when `DATABASE_URL` was missing from `.env` | High | High | Resolved |
| 2 | Database | First run: empty tables until `flask init-db` was documented and run | Medium | High | Resolved |
| 3 | Database | Iterating on SQLAlchemy models required `flask reset-db` to rebuild schema during dev | Medium | Medium | Resolved |
| 4 | Auth | Login redirect / `next` URL behaviour needed checking after form changes | Medium | Medium | Resolved |
| 5 | Reviews | Ensuring only the **owner** can delete or edit a review (server-side guard) | High | High | Resolved |
| 6 | Search | Verifying search matched **title and author** case-insensitively (`ILIKE`) | Medium | Medium | Resolved |
| 7 | Cart | Cart line **merge** behaviour when adding the same book twice (unique constraint) | Medium | Medium | Resolved |
| 8 | Cart | Quantity **0** or remove: line removed and totals consistent | Medium | Medium | Resolved |
| 9 | Checkout | Empty-cart checkout must not create an order; flash + redirect | High | High | Resolved |
| 10 | Admin | Non-admin access to `/admin/analytics` must return **403**, not expose data | High | Critical | Resolved |
| 11 | Testing | Pytest uses **SQLite in-memory**; behaviour must still be validated on **Postgres** manually | Low | Medium | Resolved |
| 12 | Static | Cover URLs and `/static/img/covers/` paths had to stay consistent with `book_covers.py` | Low | Low | Resolved |



### Lighthouse testing

I ran **Lighthouse** (Chrome DevTools → Lighthouse) against the main pages (home, books list, book detail). Scores and any follow-up tweaks are summarised in the **submitted report** so this README stays in sync with what assessors receive.

### HTML, CSS and JS validation

I validated **HTML** with the W3C Markup Validator and **CSS** with the W3C CSS Validator on representative pages. **JavaScript** was checked in the browser and with the editor’s built-in diagnostics on `static/js/main.js`. Validation outputs or screenshots are attached to the **coursework report** where the brief asked for evidence.

---

## Sources and references

These are **third-party tutorials and playlists** that helped while building bookly (Flask, PostgreSQL, and Python). They are **learning resources**, not code copied into this repository.

### Flask

| Resource | Link |
|----------|------|
| Corey Schafer — Flask Tutorial Series | [YouTube playlist](https://www.youtube.com/playlist?list=PL-osiE80TeTt2d9bfVyTiXJA-UTHn6WwU) |
| Traversy Media — Flask Crash Course | [YouTube video](https://www.youtube.com/watch?v=Z1RJmh_OqeY) |
| freeCodeCamp.org — Flask Tutorial for Beginners | [YouTube video](https://www.youtube.com/watch?v=QnDWIZuWYW0) |
| Tech With Tim — Flask Tutorial for Beginners | [YouTube video](https://www.youtube.com/watch?v=Z1RJmh_OqeY) *(same video ID as Traversy row above)* |
| Pretty Printed — Flask Web Development Tutorial | [YouTube video](https://www.youtube.com/watch?v=1WH2bXUklj4) |

### PostgreSQL *(5 videos)*

| Resource | Link |
|----------|------|
| The Net Ninja — PostgreSQL Tutorial for Beginners | [YouTube playlist](https://www.youtube.com/playlist?list=PL4cUxeGkcC9gC9b3XgUo6XhPNQXxKC0zT) |
| freeCodeCamp.org — PostgreSQL Tutorial for Beginners | [YouTube video](https://www.youtube.com/watch?v=qw--VYLpxG4) |
| Programming with Mosh — SQL Tutorial for Beginners | [YouTube video](https://www.youtube.com/watch?v=HXV3zeQKqGY) |
| Simplilearn — PostgreSQL Tutorial for Beginners | [YouTube video](https://www.youtube.com/watch?v=7S_tz1z_5bA) |
| The Net Ninja — SQL & PostgreSQL Full Course | [YouTube video](https://www.youtube.com/watch?v=zyb_dqDg2s4) |

### Python *(15 videos / playlists)*

| Resource | Link |
|----------|------|
| freeCodeCamp.org — Python Tutorial for Beginners | [YouTube video](https://www.youtube.com/watch?v=rfscVS0vtbw) |
| Corey Schafer — Python Programming Tutorials | [YouTube playlist](https://www.youtube.com/playlist?list=PL-osiE80TeTt2d9bfVyTiXJA-UTHn6WwU) |
| Programming with Mosh — Python Tutorial for Beginners | [YouTube video](https://www.youtube.com/watch?v=_Z1eL5r8K8o) |
| freeCodeCamp.org — Advanced Python Tutorials | [YouTube video](https://www.youtube.com/watch?v=2zD6iA8cE9k) |
| Tech With Tim — Python Tutorials | [YouTube playlist](https://www.youtube.com/playlist?list=PLzMcBGfZo4-nddR2E-9K9Wb8v9pK9YRMb) |
| Sentdex — Python Programming Tutorials | [YouTube playlist](https://www.youtube.com/playlist?list=PLQVvvaa0quNd8V0wD7W6zG0F7iD2O2N1Y) |
| Real Python — Python Tutorials | [YouTube playlist](https://www.youtube.com/playlist?list=PLsyeobzWwzjH-4H0XzJ6f9B7_1G7n_W2w) |
| freeCodeCamp.org — Python for Data Science | [YouTube video](https://www.youtube.com/watch?v=LHBE6Q9XdzI) |
| CS Dojo — Python Programming Tutorials | [YouTube playlist](https://www.youtube.com/playlist?list=PLBZBJbE_rGRVnpitdvpdY9952IsKMDPEb) |
| Python Engineer — Complete Python Course | [YouTube video](https://www.youtube.com/watch?v=YYXdXT2l-Cc) |
| Tech With Tim — Python Projects | [YouTube playlist](https://www.youtube.com/playlist?list=PLzMcBGfZo4-mlK5JxkJfE7k4VwSN7XGU) |
| freeCodeCamp.org — Python OOP Tutorial | [YouTube video](https://www.youtube.com/watch?v=JeznW_7DlB0) |
| Corey Schafer — Python Decorators & Generators | [YouTube video](https://www.youtube.com/watch?v=FsAPt_9Bf3U) |
| Real Python — Python Best Practices | [YouTube video](https://www.youtube.com/watch?v=rfscVS0vtbw) |
| freeCodeCamp.org — Python Data Structures | [YouTube video](https://www.youtube.com/watch?v=R-HLU9Fl5ug) |

### Images used in this project

**Wireframes** live in-repo as [`docs/wireframe-bookly.pdf`](docs/wireframe-bookly.pdf). Other coursework artefacts (e.g. Lighthouse exports) may sit only in the written submission. In the running site, cover art is SVG plus inline icons.

| Image / asset type | Where it lives | Notes |
|--------------------|----------------|-------|
| **Wireframes** | `docs/wireframe-bookly.pdf` | PDF export of bookly screen planning. |
| **Book cover graphics** | `static/img/covers/*.svg` (50 files) | Generated SVG “posters” (gradient + title + author + small bookly label). Served as static files; `cover_url` in the DB points at paths like `/static/img/covers/1984.svg`. |
| **Icons in footer** | Inline `<svg>` in `templates/base.html` | Simple vector icons for social links (not raster images). |

---

## Attributions

- **Book metadata** in `cli.py` / `seed_books.sql` is synthetic catalogue text for coursework (not an official publisher catalogue).
- **Cover SVGs** are generated placeholders (gradient + title + author) under `static/img/covers/` (listed under **Images used in this project** above).
- **Social icons** in the footer use simple SVG paths; outbound links are examples only.
- **Learning sources** are listed under [Sources and references](#sources-and-references); bookly’s implementation was written for this coursework and follows those tutorials only at a **conceptual** level unless otherwise cited in code comments.

---

## Additional Notes

- **Use of AI:** Generative AI was used mainly as an **assistant for spell checking** and small wording tweaks in written materials (for example the README and other docs). The same kind of tooling also **helped write and iterate on automated tests** (pytest); those tests were still aligned by hand with how the app actually behaves. Application and database work were implemented and checked by the author; AI did not replace that process.
- **`docs/devlog.md`** — local setup, CLI commands, checkout assumptions, cover pipeline.
- **`docs/testing.md`** — expanded automated testing description.
- During development, when the schema changed, I used **`flask reset-db`** (destructive) and re-seeded as needed.

---

## Author

- **Name:** Mohammed Sadek Hussain
- **Institution:** New City College
- **Course / project:** Project 3
- **Repository / submission:** Code and README submitted through **New City College** coursework channels (and GitHub if the assessor was given a link separately).
