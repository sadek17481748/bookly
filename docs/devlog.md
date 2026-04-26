# Development log

Short notes on how this project is wired and how to run it.

## Repository layout

- `.gitignore` excludes `.env`, virtualenv folders, and `__pycache__` so secrets and bytecode are not committed.
- `.env.example` lists the variable names you need locally (`SECRET_KEY`, `DATABASE_URL`).

## Database and models

- Tables are defined in `models.py` and mirrored in `schema.sql` for reference.
- Model order matters a little for readability: users → books → reviews → cart → orders.

## CLI commands

- `flask init-db` — `create_all()` then seed books if the table is empty.
- `flask reset-db` — drop all tables, recreate, reseed (useful after changing columns).
- `flask make-admin` — promote a registered user by email so they can open `/admin/analytics`.
- `seed_books.sql` is optional raw SQL if you prefer loading data outside the app.

## Front end

- `base.html` — skip link, header nav, flash messages, `{% block content %}`, footer.
- `static/js/main.js` — mobile nav toggle (`aria-expanded`); `data-confirm` for delete buttons.

## Automated tests

- `pytest` + Flask test client; config in `pytest.ini`, shared fixtures in `tests/conftest.py`.
- See `docs/testing.md` for the feature-to-test table markers often ask for.

## Book covers

- Generated SVGs live in `static/img/covers/` (one file per title slug from `book_covers.slug_for_title`).
- `cli.py` seeds `cover_url` like `/static/img/covers/1984.svg`. Regenerate art with `python3 tools/generate_covers.py` after changing titles.
- If your database was created before covers existed, run `flask reset-db` (or update rows) so `cover_url` is filled in.

## Checkout

- Checkout collects name and address, writes `Order` + `OrderItem`, then deletes cart rows. There is no card payment step; totals are stored in Postgres only.

## Local run

1. `python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt`
2. Create a Postgres database and user; put `DATABASE_URL` and `SECRET_KEY` in `.env`.
3. `python -m flask --app app.py init-db` then `python -m flask --app app.py run --debug`.
4. Register a user, then run `python -m flask --app app.py make-admin` if you need the analytics page.

## Deploy (Heroku-style)

- Set `SECRET_KEY`, add Postgres (host injects `DATABASE_URL`), push the app, then run `init-db` once on the server.

## Git remote

- GitHub: `https://github.com/sadek17481748/bookly.git`

## Admin analytics SQL

- “Top books” joins `order_items` to `books` and sums quantity; `coalesce` avoids nulls when there are no sales yet.
