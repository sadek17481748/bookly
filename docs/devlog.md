# Development log

Honest notes from reconstructing repository history against the final codebase.

## 2026-04-26 — Repository hygiene

- Confirmed there was no `.gitignore` in the working tree initially; added ignores for `.env`, virtualenvs, and `__pycache__` so secrets and noise never enter commits.
- Added `.env.example` so collaborators know `SECRET_KEY` and `DATABASE_URL` are required without copying real values.

