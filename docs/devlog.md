# Development log

Honest notes from reconstructing repository history against the final codebase.

## 2026-04-26 — Repository hygiene

- Confirmed there was no `.gitignore` in the working tree initially; added ignores for `.env`, virtualenvs, and `__pycache__` so secrets and noise never enter commits.
- Added `.env.example` so collaborators know `SECRET_KEY` and `DATABASE_URL` are required without copying real values.


## Models and SQLAlchemy

- Kept models ordered so relationships resolve cleanly (`User` → `Book` → `Review` → cart/order tables).

## CLI and database workflow

- `flask init-db` uses SQLAlchemy metadata; `reset-db` exists because iterative schema tweaks during development are easier with a clean recreate plus seed.
- Optional `seed_books.sql` mirrors the ORM seed list for manual DBA workflows.

## Frontend shell

- Base template uses a skip link, sticky header, and a small JS toggle for the mobile nav (`aria-expanded` updated on open/close).
- Destructive actions use `data-confirm` with a delegated click handler.

## Commerce flows

- Checkout is intentionally simple: validates name/address, persists `Order` + `OrderItem`, then clears the cart (no payment processor integration).

## Local run (summary)

1. `python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt`
2. Create Postgres database/user; set `DATABASE_URL` and `SECRET_KEY` in `.env` (copy from `.env.example`).
3. `python -m flask --app app.py init-db` then `python -m flask --app app.py run --debug`.
4. Promote an admin with `python -m flask --app app.py make-admin` after registering a user.

## Deploy (summary)

- Heroku-style: set `SECRET_KEY`, provision Postgres (`DATABASE_URL` is injected), `git push heroku main`, then `heroku run python -m flask --app app.py init-db`.

## Remote

- Intended GitHub origin: `https://github.com/sadek17481748/bookly.git` (add with `git remote add origin <url>` if not already present).

## Admin analytics

- Top books query joins `order_items` to `books`; `func.coalesce` keeps empty dashboards readable when no sales exist yet.
