# booklet (full-stack Flask + PostgreSQL)

Booklet is a simple book browsing, review, and purchasing web app built with:

- Frontend: HTML, CSS, JavaScript (server-rendered with Flask templates)
- Backend: Python (Flask)
- Database: PostgreSQL

## Features

- User registration + login/logout (password hashing)
- Browse books and view individual book details
- Reviews:
  - Logged-in users can create reviews
  - Anyone can view reviews
  - Users can delete **their own** reviews only
- Cart:
  - Add/remove items
  - Quantity updates
- Checkout:
  - Creates an order in PostgreSQL
  - Tracks which user purchased which books

## Local setup (Mac)

### 1) Install prerequisites

- Python 3.11+ recommended
- PostgreSQL 14+ recommended

### 2) Create a virtual environment and install dependencies

YOU NEED TO DO THIS STEP:

```bash
cd /Users/mohammedhussain/Desktop/bookly
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 3) Create the PostgreSQL database + user

YOU NEED TO DO THIS STEP (example values):

```bash
# If you installed Postgres via Homebrew, start it:
brew services start postgresql

# Create a DB user + database (you can change names/passwords)
psql postgres
```

In the `psql` prompt:

```sql
CREATE USER booklet_user WITH PASSWORD 'change_me';
CREATE DATABASE booklet_db OWNER booklet_user;
\q
```

### 4) Create a `.env` file

YOU NEED TO DO THIS STEP:

```bash
cd /Users/mohammedhussain/Desktop/bookly
cp .env.example .env
```

Edit `.env` and set:

- `SECRET_KEY`
- `DATABASE_URL`

Example `DATABASE_URL`:

`postgresql+psycopg2://booklet_user:change_me@localhost:5432/booklet_db`

### 5) Create tables + seed books

YOU NEED TO DO THIS STEP:

```bash
cd /Users/mohammedhussain/Desktop/bookly
source .venv/bin/activate
python -m flask --app app.py init-db
```

### 6) Run the app

YOU NEED TO DO THIS STEP:

```bash
cd /Users/mohammedhussain/Desktop/bookly
source .venv/bin/activate
python -m flask --app app.py run --debug
```

