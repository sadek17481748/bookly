# bookly — bookstore (PostgreSQL + HTML + CSS + JavaScript + Python)

## Table of Contents

- [Overview](#overview)
  - [Project goals](#project-goals)
- [Quick links (assessor)](#quick-links-assessor)
- [Features](#features)
- [User Experience (UX)](#user-experience-ux)
  - [User stories](#user-stories)
- [Wireframes](#wireframes)
- [Design](#design)
- [Technologies Used](#technologies-used)
- [File Structure](#file-structure)
- [Development](#development)
- [Deployment](#deployment)
- [Technical overview](#technical-overview)
  - [Why PostgreSQL is the technical centre of this work](#why-postgresql-is-the-technical-centre-of-this-work)
  - [Request flow overview](#request-flow-overview)
  - [Role of Flask](#role-of-flask)
  - [Project 3 scope vs what this submission demonstrates](#project-3-scope-vs-what-this-submission-demonstrates)
  - [Database (PostgreSQL)](#database-postgresql)
  - [HTML, CSS, JavaScript](#html-css-javascript)
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

**bookly** is a web app for browsing books, writing reviews, using a shopping cart, and checking out. Purchases are stored in a **PostgreSQL** database.

The site shows a realistic “small business” workflow:

- Visitors can browse catalog content **read from the database** (not hard-coded pages for each book).
- Registered users can **authenticate** securely (passwords stored as hashes, never plaintext).
- Logged-in users can create and manage **their own** reviews (including **edit** and **delete** with server-side ownership checks).
- Logged-in users can add items to a **cart**, adjust quantities, remove lines, and **check out** so that an **order** and **order line items** are written to Postgres.
- An **admin-only** analytics dashboard reads aggregate data from Postgres (counts, sums, joins) to show revenue, orders, top-selling titles, and category distribution.

### Project goals

- Demonstrate a **relational PostgreSQL** design (users, books, reviews, cart, orders).
- Show clear **end-to-end flows** where DB reads/writes show up in the UI (browse → cart → checkout → orders).
- Implement **auth and permissions** properly (hashed passwords, session login, owner-only review edit/delete, admin-only analytics).
- Keep the project easy to mark by using **server-rendered Flask** and a consistent file structure.

## Quick links (assessor)

- **Repository (README / code)**: [`sadek17481748/bookly`](https://github.com/sadek17481748/bookly)
- **Wireframes section (README anchor)**: [Wireframes](https://github.com/sadek17481748/bookly#wireframes)
- **Live app (Heroku)**: [`bookly-final-98e88d5d388e.herokuapp.com`](https://bookly-final-98e88d5d388e.herokuapp.com/)
- **Live app login page**: [Login](https://bookly-final-98e88d5d388e.herokuapp.com/login)
- **GitHub Pages (documentation site)**: [`sadek17481748.github.io/bookly`](https://sadek17481748.github.io/bookly/)
- **Closed issues (progress log)**: [GitHub Issues (closed)](https://github.com/sadek17481748/bookly/issues?q=is%3Aissue%20state%3Aclosed)

## Key UI screenshots (assessor)

Screenshots are shown below so key screens are visible directly in this README.

### Home

![Home page](docs/images/manual-testing/01-home.png)

### Books

![Books list page](docs/images/manual-testing/03-books-list.png)

### Contact

*(Screenshot to be added as `docs/images/manual-testing/02-contact.png`.)*

### Login

![Login page](docs/images/manual-testing/08-login-success.png)

### Register

![Register page](docs/images/manual-testing/06a-register-form.png)

### Analytics (admin)

![Analytics dashboard](docs/images/manual-testing/21-analytics-admin.png)

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

- **Best viewed on laptop/desktop:** the catalogue grid, checkout summary, order history, and especially the **admin analytics tables** are easier to read and compare on a wider screen (more items visible at once, less scrolling).
- **Phone/tablet support:** the site was adjusted to be usable on smaller screens (responsive CSS breakpoints stack multi-column layouts into a single column, the book detail page collapses, the footer becomes one column, and the navigation switches to a hamburger menu).

#### Responsiveness testing evidence

![Responsive testing on mobile, tablet and laptop](docs/images/validation/responsive-test-devices.png)

### User stories

**First-time / guest user**

- As a guest, I want to browse the catalogue so I can decide if I want to register.
- As a guest, I want to search by title/author so I can find a book quickly.
- As a guest, I want to see a book detail page so I can read the description and reviews.

**Registered / returning user**

- As a user, I want to register and log in so I can review and purchase books.
- As a user, I want to add books to my cart and adjust quantities so I can manage my order before checkout.
- As a user, I want to check out and then view my past orders so I can confirm the purchase was recorded.
- As a user, I want to edit/delete **my own** reviews so I can correct mistakes or remove outdated feedback.

**Admin**

- As an admin, I want to view the analytics dashboard so I can track revenue, orders, and top-selling books.
- As an admin, I want to add a new book to the catalogue (including a category and cover) so I can expand the store inventory.

### Target audience & user stories

The site is aimed at **readers** who want to browse a catalogue, read reviews, and buy books online, and at a **store admin** who needs simple sales visibility. User stories (personas, “As a … I want …”) are included in the **written report** that accompanies this submission where required by the brief.

---

## Wireframes

Low-fidelity wireframes for bookly are in this repository as a single PDF:

- **[`docs/wireframe-bookly.pdf`](docs/wireframe-bookly.pdf)** — planning layouts for the main flows (home, catalogue, book detail, auth, cart/checkout, orders, admin). The screens map to the live routes: **Home** (`/`), **Books** (`/books`), **Book detail** (`/books/<id>`), **Login / Register**, **Cart**, **Checkout**, **Orders**, and **Admin analytics** (`/admin/analytics`).

Any extra Figma links or annotated screenshots I used only in the written report stay in the **coursework appendix**; this PDF is the main wireframe file in the repo.

---

## Website build process and planning (milestones)

This section summarises **how bookly was built**, in the order features were implemented, and how the scope evolved as I worked through the coursework requirements.

### Foundation completion — **28/03**

I started by building the foundation so every later feature had a stable base:

- **Project setup**: virtual environment, dependencies, and a clean Flask project structure.
- **Configuration**: environment-based settings (`SECRET_KEY`, `DATABASE_URL`) so the same code could run locally and in a hosted environment.
- **Database first**: a PostgreSQL schema that reflects the core entities and relationships (`users`, `books`, `reviews`, `cart_items`, `orders`, `order_items`) with sensible constraints (foreign keys and uniqueness where needed).
- **Bootstrap commands and seed data**: a repeatable way to initialise the schema and seed a starter catalogue so pages were never “empty by default”.
- **Shared UI shell**: `base.html` with navigation, flash messages, and consistent layout, plus a first pass of CSS variables and reusable components.

The practical reason for doing this first was personal experience: once the database and layout are stable, every new page becomes “connect the route to the template to the query”, instead of reinventing structure on every screen.

### Milestone 1 — **31/03** (public pages + shared layout)

This milestone focused on getting the public-facing shell working end-to-end:

- **Home** and **Contact** pages built against the wireframe.
- A consistent navigation experience across pages (logged out experience first).
- Early error pages (especially **403/404**) so the site behaved clearly while routes were still being added.

### Milestone 2 — **05/04** (catalogue)

Once the shell was working, I moved onto the first database-driven feature:

- **Books list** (`/books`) populated from the database rather than static HTML.
- **Book detail** (`/books/<id>`) with price, description, and cover rendering.
- A simple **search** experience (`?q=`) to demonstrate database filtering.
- Catalogue seeding and cover URLs so the UI looked complete and consistent.

### Milestone 3 — **10/04** (authentication)

At this point scope shifted from “pages” to “user actions”:

- **Register / login / logout** implemented with hashed passwords and session management.
- Navigation updated based on authentication state (cart/orders only appear when logged in).
- Protected routes added so guest users are redirected away from actions that require an account.

### Milestone 4 — **13/04** (reviews)

Reviews were the first feature that required a mix of database relationships and security checks:

- Logged-in users can **create** reviews linked by foreign keys to both the user and the book.
- Reviews display on the book detail page.
- **Edit and delete** are restricted to the review owner with server-side checks (not only template logic).

### Milestone 5 — **16/04** (cart)

The cart is implemented as a database feature (not a session-only cart), which made scope and data modelling more important:

- Add-to-cart writes to `cart_items` and merges quantity using a uniqueness rule for one row per (user, book).
- The cart page supports quantity updates and removals with totals calculated from book prices.
- Edge cases handled (empty cart, invalid quantities) so the checkout flow would not be fragile later.

### Milestone 6 — **20/04** (checkout + orders)

This milestone turned “basket data” into “transaction history”:

- Checkout form added (minimal shipping/contact fields for coursework realism).
- Submitting checkout creates an `orders` row and multiple `order_items` rows, then clears the cart for that user.
- Orders history added so users can view what they purchased after checkout.

### Milestone 7 — **25/04** (admin analytics + final integration)

Admin analytics was the last major feature because it depends on the rest of the data model being correct:

- Admin-only route protection with a clear **403** for non-admin users.
- Dashboard queries based on aggregates and joins (revenue, order counts, top books, categories).
- A final integration pass to make flows consistent (navigation, flash messaging, and layout across templates).

### Testing and final foundation pass — **25/04**

Testing was completed alongside feature work, but the final day was a dedicated pass to make sure everything was coherent:

- **Automated testing**: pytest suite for key routes and behaviours using a fast in-memory database for repeatable runs.
- **Manual testing**: end-to-end walkthroughs on PostgreSQL (browse → auth → review → cart → checkout → orders), plus admin access checks.
- **Scope reflection**: the largest scope risks were multi-table writes (checkout) and role/ownership enforcement (reviews + admin). Those were the areas I revisited most during the final testing pass because they are easiest to “seem fine” until you try edge cases.

### Personal reflection (time constraints and improved time/communication plan)

From personal experience, project time constraints can change quickly. During this project I was **heavily delayed by personal issues**, which reduced the amount of uninterrupted time I had for development and testing. Even though the core features were completed, the delay meant I had to compress work into fewer sessions, which increases the risk of mistakes and makes progress harder to track.

In future projects, to manage my time and communication better, I would take the following steps.

#### What I would do differently next time

- **Start with a realistic schedule and visible checkpoints**
  - Break the project into small deliverables (foundation, catalogue, auth, reviews, cart, checkout, admin, testing).
  - Set short checkpoints (every 2–3 days) so progress is measurable even when time is limited.
- **Timebox work sessions and protect “core hours”**
  - Plan focused sessions (for example 60–90 minutes) with a single goal (one route, one feature, or one bug).
  - Reserve dedicated time for testing and bug fixing rather than leaving it to the end.
- **Prioritise core functionality first (MVP first)**
  - Build the “must-have” user journey early: browse → login → cart → checkout → orders.
  - Treat admin analytics and extra polish as optional until the main flow is stable.
- **Track decisions and changes as I go**
  - Keep short notes after each session (what was done, what broke, what is next).
  - Record database changes and why they were made so I do not lose time re-learning decisions later.
- **Communicate earlier when delays happen**
  - If I hit a personal issue or a schedule slip, I would communicate it earlier rather than trying to recover silently.
  - Share a revised plan (what will be completed first, and what may be reduced) so expectations stay clear.
- **Reduce risk by testing continuously**
  - Run automated tests regularly (not only at the end).
  - Do quick manual checks after each major feature (especially multi-table writes like checkout and role/ownership rules).

#### What I learned

This project reinforced that the biggest risk under time pressure is not writing code—it is losing structure: forgetting what changed, delaying testing, and trying to complete too many features at once. A clearer schedule, earlier communication, and smaller planned deliverables would make future projects more controlled and less stressful, even if delays happen.

---

## Design

### Visual language

- **Dark theme** with CSS variables (`--bg`, `--panel`, `--text`, `--brand`, `--danger`, etc.) in `static/css/styles.css` for consistent colour and spacing.
- **Gradients** on hero and buttons for depth; **cards** with subtle borders and shadows for content grouping.
- **Typography:** system UI stack (`ui-sans-serif`, `system-ui`, …) for fast loading and native feel.

### Colour scheme (and why)

The site uses a **dark, high-contrast** palette to keep long reading sessions comfortable and to make book covers and cards stand out clearly.

- **Background (`--bg`)**: deep navy used as the base canvas so content panels feel separated without heavy borders.
- **Panels (`--panel`)**: slightly lighter navy for cards and sections to create depth while staying consistent with the dark theme.
- **Text (`--text`) + muted text (`--muted`)**: bright off-white for readability, with a muted variant for secondary information (author names, timestamps, hints).
- **Primary brand (`--brand`)**: purple accent for primary actions and key highlights (buttons, links) to give the UI a recognisable identity.
- **Secondary accent (`--brand2`)**: green accent used sparingly to add contrast in gradients and to avoid a single-colour interface.
- **Danger (`--danger`)**: pink/red accent reserved for destructive actions (delete/remove) so risk actions are visually obvious.

These choices are implemented as CSS variables at the top of `static/css/styles.css` so the palette is consistent across the whole site and easy to adjust in one place.

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

**Frontend libraries note:** No UI framework such as **Bootstrap** was used. The UI is custom CSS in `static/css/styles.css` and a small amount of vanilla JavaScript in `static/js/main.js` (no jQuery).

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
| `cli.py` | `flask init-db`, `reset-db`, `make-admin`; seeds books and back-fills `cover_url` values |
| `templates/` | Jinja2 HTML (includes admin pages) |
| `templates/admin_add_book.html` | Admin-only “Add book” form (category + cover selection) |
| `static/css/styles.css` | Site styles |
| `static/js/main.js` | Nav toggle + confirm helper |
| `static/img/covers/` | Cover assets used by the catalogue (SVG placeholders + any added raster covers) |
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
| `docs/legacy-code.md` | Small “before → after” code snapshots for assessor review |
| `docs/wireframe-bookly.pdf` | Wireframes (PDF) for main screens and flows |
| `docs/images/validation/` | Evidence screenshots (Lighthouse, W3C validators, JSHint, responsiveness, 404) |

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

### Troubleshooting (local Postgres setup)

- **`password authentication failed for user ...`**
  - This usually means `DATABASE_URL` in `.env` still has placeholder values or the Postgres user password does not match.
  - Fix by updating `.env` to a real connection string and (re)setting the user password in Postgres, for example:

```sql
ALTER USER bookly_user WITH PASSWORD 'bookly_pass';
```

- **Commands typed inside `psql` by mistake**
  - If the prompt looks like `postgres=#` or `postgres-#`, you are inside Postgres interactive mode.
  - Exit with `\q` to return to the normal terminal prompt before running:
    - `python -m flask --app app.py init-db`
    - `python -m flask --app app.py run --debug`

### Promote an admin user

After I registered a user in the browser:

```bash
python -m flask --app app.py make-admin
```

The command prompts for an email; I used the account I wanted to promote so `is_admin` is set and `/admin/analytics` unlocks.

### Assessor / invigilator login (analytics access)

To make marking simpler, I created a dedicated admin account for the analytics dashboard:

- **Email:** `analytics@testemail.com`
- **Password:** `test123`

After logging in, the admin analytics dashboard is available at **`/admin/analytics`**.

**Note (live Heroku app):** The Heroku deployment uses its own Postgres database, so the account must be **registered on the live site** and then promoted to admin (set `users.is_admin = true`). This can be done using `heroku pg:psql` or by running the existing CLI command (`make-admin`) against the Heroku app.

### Automated tests (no Postgres required for pytest)

```bash
source .venv/bin/activate
pytest -v
```

Tests use **SQLite in-memory** via `tests/conftest.py` so they run quickly; I still demonstrated PostgreSQL using the steps above. Full mapping: **`docs/testing.md`**.

---

## Deployment

I deployed bookly to Heroku and used Heroku Postgres for the production database.

### Heroku deployment (step-by-step)

**Install and login (local machine):**

```bash
brew tap heroku/brew && brew install heroku
heroku login
```

**Create/link the Heroku app:**

```bash
cd /path/to/bookly-final
heroku create bookly-final
heroku git:remote -a bookly-final
```

**Add a managed Postgres database (sets `DATABASE_URL`):**

```bash
heroku addons:create heroku-postgresql:essential-0 -a bookly-final
```

**Set required config vars:**

```bash
heroku config:set SECRET_KEY="a-long-random-string" -a bookly-final
```

**Deploy code and initialise the database (create tables + seed):**

```bash
git push heroku main
heroku run -a bookly-final -- python3 -m flask --app app.py init-db
heroku open -a bookly-final
```

**Production notes:**

- `Procfile` runs the app with **Gunicorn** (`gunicorn app:app`).
- Heroku provides `DATABASE_URL` in the `postgres://...` form; the app normalises this to `postgresql://...` for SQLAlchemy compatibility in `config.py`.
- During deployment I used `heroku logs --tail -a bookly-final` to diagnose startup issues.

**Live site URL (Heroku):**

- `https://bookly-final-98e88d5d388e.herokuapp.com/`

### GitHub repository + Pages

- I created the GitHub repository and added the project documentation (`README.md`).
- To publish the documentation on GitHub Pages, I opened **Settings → Pages**, selected **Deploy from a branch**, chose **`main`** as the source, and saved to generate the Pages site.
- I also used GitHub **Issues** to log issues and user stories, and to track progress throughout development.

---

## Technical overview

### Why PostgreSQL is the technical centre of this work

PostgreSQL is a core part of the project:

- **Connection:** the app reads `DATABASE_URL` from the environment (`config.py`, `.env.example`). In development this pointed at a **local Postgres** instance; on Heroku it used the **managed Postgres** add-on URL.
- **Integrity:** foreign keys tie reviews to users and books, cart lines to users and books, order items to orders and books. `schema.sql` lists the same structure for reference and marking.
- **Meaningful writes:** checkout creates an `orders` row and multiple `order_items` rows, then deletes `cart_items` for that user—i.e. a **multi-table write** I verified in `psql` and other SQL clients during development.
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

### Project 3 scope vs what this submission demonstrates

For **Project 3**, the emphasis was typically on **PostgreSQL**—designing tables, relationships, and queries—often with a **lighter** presentation layer than a full production-style web stack.

This project **goes beyond** that minimal presentation bar and is implemented as a **small full-stack, server-rendered application**:

| Typical Project 3 focus | What bookly adds (and why) |
|-------------------------|----------------------------|
| SQL scripts, ER thinking, maybe a thin UI | **End-to-end paths**: browser → Flask routes → SQLAlchemy → **PostgreSQL** → HTML response. That makes the database work **visible and testable** as part of a real use case (browse → cart → checkout → orders). |
| Less emphasis on auth, sessions, deployment | **Flask-Login** sessions, **environment-based configuration**, and a **Heroku-style** deployment story so Postgres is not “theory only” but runnable **locally and** on a hosted database. |

**Why this still fits the marking criteria**

1. **PostgreSQL remains the source of truth.** Users, books, reviews, cart rows, orders, and order items all live in Postgres. The ORM generates SQL; constraints (foreign keys, uniqueness on cart lines) match standard relational design taught on the course.
2. **A thin static page** can show a `SELECT` result, but it does not demonstrate **transactions across steps** (cart updates, checkout clearing the cart while inserting orders) or **authorization** (only the review owner can delete). Those behaviours need **application logic** tied to the database.
3. **Separation of concerns is still clear:** `schema.sql` documents the DDL; `models.py` mirrors it for SQLAlchemy; `books.py`, `cart.py`, `orders.py` show **which HTTP actions cause which writes** to Postgres.

For assessment, **`schema.sql`**, the **`models.py` ↔ table mapping**, and **`docs/devlog.md`** (setup notes) document the relational design and local setup. The Flask routes and blueprints show **how** that PostgreSQL design is exercised in practice (browse, cart, checkout, admin reads).

### HTML, CSS, JavaScript

- **HTML / Jinja2** under `templates/` builds pages and loops (e.g. book grid, review list).
- **CSS** in `static/css/styles.css` defines layout, dark theme, responsive grids, forms, and admin tables.
- **JavaScript** in `static/js/main.js` adds progressive enhancements (nav toggle, confirm before destructive POSTs). **Security rules stay on the server** (e.g. “only delete your own review” is enforced in Python, not only in JS).

### Why this approach?

Server-rendered Flask keeps the database work clear: every important screen is backed by a query or a write to **PostgreSQL**. This matches Project 3 learning outcomes while still being a complete small app.

---

## Testing and Bugs

### Manual testing

I complemented automated tests with manual runs in the browser, recording **what I did**, **what I expected**, and **what happened**. The table below is the checklist I used; I filled **Pass/Fail**, **Notes**, and captured screenshots in `docs/images/manual-testing/`.

| # | Area | Step | Expected | Pass/Fail | Notes | Screenshot evidence |
|---|------|------|----------|-----------|-------|-------------------|
| 1 | Public | Open `/` | Home loads; branding and hero visible | Pass |  | [01-home](docs/images/manual-testing/01-home.png) |
| 2 | Public | Open `/contact` | Contact content loads | Pass | Screenshot pending | `docs/images/manual-testing/02-contact.png` |
| 3 | Public | Open `/books` | Catalog or empty state loads | Pass |  | [03-books-list](docs/images/manual-testing/03-books-list.png) |
| 4 | Public | Use search `?q=` with a known title | Matching books appear | Pass |  | [04-search](docs/images/manual-testing/04-search.png)<br>[04b-search-no-results](docs/images/manual-testing/04b-search-no-results.png) |
| 5 | Public | Open a book detail URL | Title, author, price, description | Pass |  | [05-book-detail](docs/images/manual-testing/05-book-detail.png) |
| 6 | Auth | Register a new user | Redirect to books; flash success | Pass |  | [06a-register-form](docs/images/manual-testing/06a-register-form.png)<br>[06-register-success](docs/images/manual-testing/06-register-success.png) |
| 7 | Auth | Log out | Session cleared; home or login | Pass | Screenshot pending | `docs/images/manual-testing/07-logout.png` |
| 8 | Auth | Log in with correct password | Redirect; flash success | Pass |  | [08-login-success](docs/images/manual-testing/08-login-success.png) |
| 9 | Auth | Log in with wrong password | Stays on login; flash error | Pass | Screenshot pending | `docs/images/manual-testing/09-login-fail.png` |
| 10 | Auth | Register duplicate email | Error; no duplicate user | Pass |  | [10-register-duplicate](docs/images/manual-testing/10-register-duplicate.png) |
| 11 | Reviews | While logged out, open book detail | No POST review without login | Pass | Screenshot pending | `docs/images/manual-testing/11-reviews-guest.png` |
| 12 | Reviews | Post a review (logged in) | Review appears on page | Pass |  | [12-review-created](docs/images/manual-testing/12-review-created.png) |
| 13 | Reviews | Edit **your** review | Updated text/rating shown | Pass |  | [13-review-edit](docs/images/manual-testing/13-review-edit.png) |
| 14 | Reviews | Delete **your** review | Review removed | Pass |  | [14-review-delete](docs/images/manual-testing/14-review-delete.png) |
| 15 | Reviews | Attempt to delete another user’s review (second account) | Blocked with message | Pass |  | [15-review-owner-block](docs/images/manual-testing/15-review-owner-block.png) |
| 16 | Cart | Add book to cart | Line appears with correct title/qty | Pass |  | [16-cart-add](docs/images/manual-testing/16-cart-add.png) |
| 17 | Cart | Change quantity / remove line | Totals and rows update | Pass |  | [17-cart-update-remove](docs/images/manual-testing/17-cart-update-remove.png) |
| 18 | Cart | Checkout with empty cart | Error flash; redirect to cart | Pass | Screenshot pending | `docs/images/manual-testing/18-checkout-empty.png` |
| 19 | Orders | Checkout with items | Order on Orders page; cart empty | Pass |  | [19-checkout-success](docs/images/manual-testing/19-checkout-success.png)<br>[19b-orders-page](docs/images/manual-testing/19b-orders-page.png) |
| 20 | Admin | Open `/admin/analytics` as normal user | 403 Forbidden page | Pass | Screenshot pending | `docs/images/manual-testing/20-analytics-403.png` |
| 21 | Admin | Same as admin user | Dashboard metrics load | Pass |  | [21-analytics-admin](docs/images/manual-testing/21-analytics-admin.png) |
| 22 | Admin | Add a new book via Analytics → Add book | Book created and visible in catalogue | Pass |  | [22-admin-add-book](docs/images/manual-testing/22-admin-add-book.png)<br>[23-admin-book-added](docs/images/manual-testing/23-admin-book-added.png) |

#### 404 page (assessor note + evidence)

- **Where to find it:** click **Sitemap** in the footer (route: **`/sitemap`**). This route is intentionally not implemented so the custom 404 page is shown.

![Custom 404 page](docs/images/validation/404-page.png)

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
| 1 | Authentication | `GET /register` loads | Pass | `test_register_get_ok` |
| 2 | Authentication | `GET /login` loads | Pass | `test_login_get_ok` |
| 3 | Authentication | Register → logout → login works end-to-end | Pass | `test_register_login_flow` |
| 4 | Authentication | Register rejected when passwords do not match | Pass | `test_register_password_mismatch` |
| 5 | Authentication | Login rejected when password is wrong | Pass | `test_login_bad_password` |
| 6 | Books & reviews | Search returns matching book | Pass | `test_books_search_param_ok` |
| 7 | Books & reviews | Guest cannot POST a review (redirect to login) | Pass | `test_create_review_requires_login` |
| 8 | Books & reviews | Logged-in user can create a review | Pass | `test_create_review_ok` |
| 9 | Cart & orders | Guest cannot open cart (redirect) | Pass | `test_cart_requires_login` |
| 10 | Cart & orders | Logged-in user can add a book to cart | Pass | `test_add_to_cart_ok` |
| 11 | Cart & orders | Checkout with empty cart is handled safely | Pass | `test_checkout_empty_cart_redirects` |
| 12 | Admin | Guest cannot open analytics (redirect) | Pass | `test_admin_analytics_requires_login` |
| 13 | Admin | Non-admin receives **403** on analytics | Pass | `test_admin_analytics_forbidden_for_normal_user` |
| 14 | Admin | Admin user receives **200** and dashboard content | Pass | `test_admin_analytics_ok_for_admin` |
| 15 | Public pages | Home page loads with expected content | Pass | `test_home_ok` |
| 16 | Public pages | Contact page loads | Pass | `test_contact_ok` |
| 17 | Public pages | Books list page loads | Pass | `test_books_list_empty_ok` |
| 18 | Public pages | Unknown book id returns **404** | Pass | `test_book_detail_404` |
| 19 | Public pages | Book detail shows seeded sample book | Pass | `test_book_detail_ok` |
| 20 | Public pages | Global stylesheet is served (`/static/css/styles.css`) | Pass | `test_static_css_served` |

### Bugs encountered during development

The table below is a **bug / issue log** in the style used for coursework: it records problems **encountered while building bookly**, how serious they were, and that they were **resolved**. It is **not** a list of current security defects—the shipped app uses **Werkzeug password hashing** and server-side checks as implemented in `models.py` and the blueprints.

### Use of AI (assistance log)

This table lists where AI-assisted help was used during development and documentation. The final code and write-up were still checked, edited, and tested manually to match how the project actually works.

| Area / section | What AI assistance was used for | Notes / checks I still did |
|---|---|---|
| **README + docs** (`README.md`, `docs/*.md`) | Spell-checking, rephrasing for clarity, tightening wording, and structuring sections (TOC, headings). | I verified all steps and claims against the actual repository contents and deployment flow. |
| **Pytest suite** (`tests/`) | Drafting test structure and suggesting assertions/fixtures for Flask routes. | I ran the tests, fixed failures, and aligned each test to real routes and behaviours. |
| **Python (Flask / SQLAlchemy)** (`app.py`, blueprints, `cli.py`) | Spot-checking patterns (blueprints, decorators, error handlers) and suggesting safer validation/guard logic. | I implemented the logic, tested flows in-browser, and confirmed DB writes/reads in Postgres. |
| **HTML/Jinja templates** (`templates/`) | Suggesting layout tweaks and accessibility improvements (labels, alt text, ARIA). | I checked pages visually, verified navigation flows, and ensured server-side checks remained in Python. |
| **CSS/JS** (`static/css/styles.css`, `static/js/main.js`) | Minor suggestions for responsiveness and small JS helpers (nav toggle, confirm). | I validated behaviour on multiple screen sizes and confirmed no critical console errors. |

| Bug number | Area | Description | Severity | Priority | Solutions | Status |
|------------|------|-------------|----------|----------|-----------|--------|
| 1 | Environment | App crashed on startup when `DATABASE_URL` was missing from `.env` | High | High | Add `.env` using `.env.example`, set `DATABASE_URL` and `SECRET_KEY`, then restart the server. | Resolved |
| 2 | Database | First run: empty tables until `flask init-db` was documented and run | Medium | High | Run `python -m flask --app app.py init-db` to create tables and seed the catalogue. | Resolved |
| 3 | Database | Iterating on SQLAlchemy models required `flask reset-db` to rebuild schema during dev | Medium | Medium | Run `python -m flask --app app.py reset-db` after model/schema changes to drop/recreate tables and reseed. | Resolved |
| 4 | Auth | Login redirect / `next` URL behaviour needed checking after form changes | Medium | Medium | Preserve `next` in the login form/action and redirect to `next` after successful login; verify with manual tests. | Resolved |
| 5 | Reviews | Ensuring only the **owner** can delete or edit a review (server-side guard) | High | High | Add server-side ownership checks (`review.user_id == current_user.id`) in edit/delete routes; hide buttons in templates as a secondary UX measure. | Resolved |
| 6 | Search | Verifying search matched **title and author** case-insensitively (`ILIKE`) | Medium | Medium | Use SQLAlchemy `ilike` filters on `Book.title` and `Book.author` and test with mixed-case queries. | Resolved |
| 7 | Cart | Cart line **merge** behaviour when adding the same book twice (unique constraint) | Medium | Medium | Enforce one row per `(user_id, book_id)` and merge quantities in `add_to_cart`; verify with repeated adds. | Resolved |
| 8 | Cart | Quantity **0** or remove: line removed and totals consistent | Medium | Medium | Treat quantity < 1 as delete; recalculate subtotal from remaining lines and confirm via manual tests. | Resolved |
| 9 | Checkout | Empty-cart checkout must not create an order; flash + redirect | High | High | Block checkout when cart is empty; flash an error and redirect back to the cart page. | Resolved |
| 10 | Admin | Non-admin access to `/admin/analytics` must return **403**, not expose data | High | Critical | Add an admin-only decorator that checks `current_user.is_admin`; abort with 403 for non-admins. | Resolved |
| 11 | Testing | Pytest uses **SQLite in-memory**; behaviour must still be validated on **Postgres** manually | Low | Medium | Run pytest on SQLite for speed, and separately verify key flows manually against Postgres (checkout, admin, ownership checks). | Resolved |
| 12 | Static | Cover URLs and `/static/img/covers/` paths had to stay consistent with `book_covers.py` | Low | Low | Standardise `cover_url` values to `/static/img/covers/<slug>.svg` and keep slugs generated by `book_covers.py`. | Resolved |
| 13 | Database / Setup | Local run failed with `password authentication failed` because `.env` still contained placeholder `DATABASE_URL` values (`USER:PASSWORD@.../DBNAME`). Resolved by creating/updating the Postgres role/database and ensuring commands like `python -m flask ...` were run in the terminal (not inside `psql`). | Medium | High | Update `.env` with a real `DATABASE_URL`; set/reset the Postgres password with `ALTER USER ... WITH PASSWORD ...`; exit `psql` with `\\q` before running Flask commands. | Resolved |
| 14 | Static / Seed data | Book cover images did not appear on cards because the `books` table already contained older seeded rows with empty `cover_url` values, and `flask init-db` only seeds when the catalogue is empty. Resolved by resetting and re-seeding (`flask reset-db`) so seeded books include correct `/static/img/covers/*.svg` paths. | Low | Medium | Run `python -m flask --app app.py reset-db` to reseed with covers (or update existing `books.cover_url` values if data must be kept). | Resolved |



### Lighthouse testing

I ran **Lighthouse** (Chrome DevTools → Lighthouse) against the main pages (home, books list, book detail). Scores and any follow-up tweaks are summarised in the **submitted report** so this README stays in sync with what assessors receive.

#### Lighthouse report screenshot (Home)

![Lighthouse results - Home](docs/images/validation/lighthouse-home.png)

### HTML, CSS and JS validation

I validated **HTML** with the W3C Markup Validator and **CSS** with the W3C CSS Validator on representative pages. **JavaScript** was checked using JSHint and with the editor’s built-in diagnostics on `static/js/main.js`.

#### W3C CSS validation (no errors)

![W3C CSS validator - no errors](docs/images/validation/w3c-css-valid.png)

#### W3C HTML validation results

![W3C HTML validator results](docs/images/validation/w3c-html-results.png)

#### JSHint results (`static/js/main.js`)

![JSHint results](docs/images/validation/jshint-main-js.png)

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

# Sources for Python

This document compiles helpful references and sources related to Flask, SQLAlchemy, environment management, security, and best practices for Python web development.

---

## Flask Application Structure and Best Practices

- **Application Factory Pattern**  
  https://flask.palletsprojects.com/en/2.3.x/patterns/appfactories/

- **Flask Configuration Management**  
  https://flask.palletsprojects.com/en/2.3.x/config/

- **Using python-dotenv for Environment Variables**  
  https://github.com/theskumar/python-dotenv

- **BluePrints in Flask**  
  https://flask.palletsprojects.com/en/2.3.x/blueprints/

- **Error Handling in Flask**  
  https://flask.palletsprojects.com/en/2.3.x/errorhandling/

- **Registering CLI Commands in Flask**  
  https://flask.palletsprojects.com/en/2.3.x/cli/

- **Deployment Considerations (Gunicorn, Heroku)**  
  https://devcenter.heroku.com/categories/python

---

## Flask-Login and User Authentication

- **Flask-Login Documentation**  
  https://flask-login.readthedocs.io/en/latest/

- **Password Hashing with Werkzeug**  
  https://werkzeug.palletsprojects.com/en/2.3.x/utils/#module-werkzeug.security

- **Security Best Practices in Flask**  
  - Use HTTPS in production  
  - Validate email addresses properly  
  - Protect against CSRF (consider flask-wtf)  
  https://owasp.org/www-community/controls/Session_Management  
  https://owasp.org/www-community/Input_Validation

---

## Flask and SQLAlchemy ORM

- **SQLAlchemy ORM Documentation**  
  https://docs.sqlalchemy.org/en/14/orm/

- **Creating and Dropping Tables**  
  https://docs.sqlalchemy.org/en/14/orm/session_api.html#sqlalchemy.orm.session.Session

- **Application-wide Database Object Pattern**  
  https://flask-sqlalchemy.palletsprojects.com/en/3.0.x/contexts/#application-setup

- **Querying and Filtering**  
  https://docs.sqlalchemy.org/en/14/orm/query.html

---

## Flask Static Files and URL Handling

- **Flask Static Files**  
  https://flask.palletsprojects.com/en/2.3.x/quickstart/#static-files

- **URL Building with `url_for`**  
  https://flask.palletsprojects.com/en/2.3.x/templating/#url-for

---

## Database and Environment Configuration

- **Using Environment Variables for Secrets**  
  https://12factor.net/config

- **Heroku DATABASE_URL Compatibility**  
  - Heroku Postgres URL: https://devcenter.heroku.com/articles/heroku-postgresql#connecting-in-python  
  - SQLAlchemy URL Schemes: https://docs.sqlalchemy.org/en/14/core/engines.html#database-urls

---

## Flask CLI Command Development

- **Flask CLI Documentation**  
  https://flask.palletsprojects.com/en/2.3.x/cli/

- **Creating Custom CLI Commands**  
  https://flask.palletsprojects.com/en/2.3.x/cli/#custom-commands

- **Seeding Data and Migrations**  
  - https://realpython.com/building-a-flask-and-sqlalchemy-application/  
  - https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-vii-webforms

---

## Common Security and Best Practices

- **Input Validation and Sanitization**  
  https://owasp.org/www-community/Input_Validation

- **Cross-site Request Forgery (CSRF) Protection**  
  https://flask-wtf.readthedocs.io/en/stable/csrf.html

- **Session Security and Management**  
  https://owasp.org/www-community/controls/Session_Management

---

## Miscellaneous

- **Slug Creation and String Normalization in Python**  
  https://slugify.readthedocs.io/en/latest/  
  https://docs.python.org/3/library/re.html  
  https://docs.python.org/3/library/stdtypes.html#str.casefold

- **Path Handling with pathlib**  
  https://docs.python.org/3/library/pathlib.html

---

This collection aims to provide authoritative sources to deepen your understanding and guide best practices in Python web development with Flask and SQLAlchemy.

### Images used in this project

**Wireframes** live in-repo as [`docs/wireframe-bookly.pdf`](docs/wireframe-bookly.pdf). Other coursework artefacts (e.g. Lighthouse exports) may sit only in the written submission. In the running site, cover art is SVG plus inline icons.

| Image / asset type | Where it lives | Notes |
|--------------------|----------------|-------|
| **Wireframes** | `docs/wireframe-bookly.pdf` | PDF export of bookly screen planning. |
| **Book cover graphics** | `static/img/covers/*.svg` (50 files) | Generated SVG “posters” (gradient + title + author + small bookly label). Served as static files; `cover_url` in the DB points at paths like `/static/img/covers/1984.svg`. |
| **Icons in footer** | Inline `<svg>` in `templates/base.html` | Simple vector icons for social links (not raster images). |

### Image credits

The catalogue uses cover images to make the UI feel closer to a real storefront. Where a real-world cover thumbnail was used, the source is credited below.

| Asset | Source / link | Credit / licence note |
|------|---------------|------------------------|
| **Book cover images** (`static/img/covers/*.{png,jpg,svg}`) | *(links to be added)* | Local cover assets served from `static/img/covers/`. Individual external sources are credited in the rows below. |
| **Cover source (Where the Crawdads Sing)** | [Wikipedia page](https://en.wikipedia.org/wiki/Where_the_Crawdads_Sing) | Source link for the cover image used. |
| **Cover source (The Help)** | [Wikipedia page](https://en.wikipedia.org/wiki/The_Help) | Source link for the cover image used. |
| **Cover source (Me Before You)** | [Wikipedia page](https://en.wikipedia.org/wiki/Me_Before_You) | Source link for the cover image used. |
| **Cover source (The Road)** | [Wikipedia page](https://en.wikipedia.org/wiki/The_Road) | Source link for the cover image used. |
| **Cover source (Life of Pi)** | [Wikipedia page](https://en.wikipedia.org/wiki/Life_of_Pi) | Source link for the cover image used. |
| **Cover source (The Kite Runner)** | [Wikipedia page](https://en.wikipedia.org/wiki/The_Kite_Runner) | Source link for the cover image used. |
| **Cover source (A Thousand Splendid Suns)** | [Wikipedia page](https://en.wikipedia.org/wiki/A_Thousand_Splendid_Suns) | Source link for the cover image used. |
| **Cover source (The Alchemist)** | [Wikipedia page](https://en.wikipedia.org/wiki/The_Alchemist_(novel)) | Source link for the cover image used. |
| **Cover source (The Woman in the Window)** | [Wikipedia page](https://en.wikipedia.org/wiki/The_Woman_in_the_Window) | Source link for the cover image used. |
| **Cover source (The Reversal)** | [Wikipedia page](https://en.wikipedia.org/wiki/The_Reversal) | Source link for the cover image used. |
| **Cover source (And Then There Were None)** | [Wikipedia page](https://en.wikipedia.org/wiki/And_Then_There_Were_None) | Source link for the cover image used. |
| **Cover source (Big Little Lies)** | [Wikipedia page](https://en.wikipedia.org/wiki/Big_Little_Lies_(novel)) | Source link for the cover image used. |
| **Cover source (The Silent Patient)** | [Wikipedia page](https://en.wikipedia.org/wiki/The_Silent_Patient) | Source link for the cover image used. |
| **Cover source (In the Woods)** | [Wikipedia page](https://en.wikipedia.org/wiki/In_the_Woods) | Source link for the cover image used. |
| **Cover source (Gone Girl)** | [Wikipedia page](https://en.wikipedia.org/wiki/Gone_Girl_(novel)) | Source link for the cover image used. |
| **Cover source (The Girl with the Dragon Tattoo)** | [Wikipedia page](https://en.wikipedia.org/wiki/The_Girl_with_the_Dragon_Tattoo) | Source link for the cover image used. |
| **Cover source (The Da Vinci Code)** | [Wikipedia page](https://en.wikipedia.org/wiki/The_Da_Vinci_Code) | Source link for the cover image used. |
| **Cover source (Ready Player One)** | [Wikipedia page](https://en.wikipedia.org/wiki/Ready_Player_One) | Source link for the cover image used. |
| **Cover source (Frankenstein)** | [Wikipedia page](https://en.wikipedia.org/wiki/Frankenstein) | Source link for the cover image used. |
| **Cover source (The Martian)** | [Wikipedia page](https://en.wikipedia.org/wiki/The_Martian) | Source link for the cover image used. |
| **Cover source (Ender’s Game)** | [Wikipedia page](https://en.wikipedia.org/wiki/Ender%27s_Game) | Source link for the cover image used. |
| **Cover source (Dune)** | [Wikipedia page](https://en.wikipedia.org/wiki/Dune_(novel)) | Source link for the cover image used. |
| **Cover source (The Hobbit)** | [Wikipedia page](https://en.wikipedia.org/wiki/The_Hobbit) | Source link for the cover image used. |
| **Cover source (The Great Gatsby)** | [Wikipedia page](https://en.wikipedia.org/wiki/The_Great_Gatsby) | Source link for the cover image used. |
| **Wireframes PDF** (`docs/wireframe-bookly.pdf`) | N/A | Created by me during the planning phase. |
| **Footer icons** (inline `<svg>`) | *(links to be added if applicable)* | Vector icons embedded directly in templates. |

---

## Attributions

- **Book metadata** in `cli.py` / `seed_books.sql` is synthetic catalogue text for coursework (not an official publisher catalogue).
- **Cover assets** live under `static/img/covers/` (a mix of SVG placeholders and raster cover images where credited in the Image credits section).
- **Social icons** in the footer use simple SVG paths; outbound links are examples only.
- **Learning sources** are listed under [Sources and references](#sources-and-references); bookly’s implementation was written for this coursework and follows those tutorials only at a **conceptual** level unless otherwise cited in code comments.

---

## Additional Notes

- **Use of AI:** Generative AI was used as an **assistant** during development (mainly spell-checking and improving the clarity of documentation). It also helped with **drafting and iterating on automated tests** and discussing approaches for parts of the Python/Flask code (validation, structure, and edge cases). The final implementation was still **written/edited, verified, and tested by me**, and any AI suggestions were only kept when they matched the project’s real behaviour. A concise log of AI-assisted areas is included in **Testing and Bugs → Use of AI (assistance log)**.
- **`docs/devlog.md`** — local setup, CLI commands, checkout assumptions, cover pipeline.
- **`docs/testing.md`** — expanded automated testing description.
- During development, when the schema changed, I used **`flask reset-db`** (destructive) and re-seeded as needed.

---

## Author

- **Name:** Mohammed Sadek Hussain
- **Institution:** New City College
- **Course / project:** Project 3
- **Repository / submission:** Code and README submitted through **New City College** coursework channels (and GitHub if the assessor was given a link separately).
