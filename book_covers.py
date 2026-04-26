# Map each catalog book title to a static cover file under static/img/covers/.

from __future__ import annotations

import re


def slug_for_title(title: str) -> str:
    """Filename slug (ASCII, hyphens) matching generated SVG names."""
    s = title.casefold()
    for ch in (
        "\u2019",
        "\u2018",
        "'",
        "`",
    ):
        s = s.replace(ch, "")
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return s.strip("-")


def cover_static_url(title: str) -> str:
    """URL path served by Flask static (see static/img/covers/*.svg)."""
    return f"/static/img/covers/{slug_for_title(title)}.svg"
