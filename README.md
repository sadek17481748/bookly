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
