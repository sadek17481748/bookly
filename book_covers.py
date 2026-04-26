# ============================================================
# BOOK COVER URL HELPERS
# - Maps a book title to a stable SVG filename slug
# - Used by seeds so `cover_url` points at static/img/covers/*.svg
# ============================================================

from __future__ import annotations

import re


def slug_for_title(title: str) -> str:
    """Filename slug (ASCII, hyphens) matching generated SVG names."""
    # ================= NORMALISE + STRIP PUNCTUATION =================
    s = title.casefold()
    for ch in (
        "\u2019",
        "\u2018",
        "'",
        "`",
    ):
        s = s.replace(ch, "")
    # ================= KEEP ASCII + DASH SEPARATORS =================
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return s.strip("-")


def cover_static_url(title: str) -> str:
    """URL path served by Flask static (see static/img/covers/*.svg)."""
    # ================= BUILD STATIC PATH =================
    return f"/static/img/covers/{slug_for_title(title)}.svg"
