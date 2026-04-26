-- PostgreSQL schema for booklet
-- You can run this manually, but the app's CLI command `flask init-db`
-- will create the same tables automatically using SQLAlchemy.

CREATE TABLE IF NOT EXISTS users (
  id SERIAL PRIMARY KEY,
  email VARCHAR(255) UNIQUE NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  is_admin BOOLEAN NOT NULL DEFAULT FALSE,
  created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS books (
  id SERIAL PRIMARY KEY,
  title VARCHAR(255) NOT NULL,
  author VARCHAR(255) NOT NULL,
  category VARCHAR(255) NOT NULL DEFAULT 'Uncategorized',
  price_cents INTEGER NOT NULL,
  description TEXT NOT NULL DEFAULT '',
  cover_url VARCHAR(1024),
  created_at TIMESTAMP NOT NULL DEFAULT NOW()
);
