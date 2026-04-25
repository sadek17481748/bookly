# Shared pytest fixtures: in-memory DB + Flask test client.

from __future__ import annotations

import os

# These must exist before `app` is imported (app.py calls create_app() at import time).
os.environ.setdefault("SECRET_KEY", "pytest-secret-not-for-production")
