#!/usr/bin/env python3
"""Generate static/img/covers/*.svg for every Book() seed title in cli.py."""

from __future__ import annotations

import hashlib
import re
import sys
import xml.sax.saxutils as xml_esc
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

# Gradient pairs (dark theme, readable white text)
PALETTES = [
    ("#1e3a5f", "#0f172a"),
    ("#3d2a5c", "#1a1030"),
    ("#1f4e3d", "#0d2818"),
    ("#4a2c2a", "#1f0f0e"),
    ("#2d3a4a", "#151c26"),
    ("#3d1f4e", "#180a22"),
    ("#1a3d3d", "#0a2222"),
    ("#4a3a1f", "#221a0a"),
    ("#2a2a4e", "#12122a"),
    ("#1f3d4a", "#0a1a22"),
]


def escape_text(s: str) -> str:
    return xml_esc.escape(s)


def main() -> None:
    from book_covers import slug_for_title

    cli = (ROOT / "cli.py").read_text(encoding="utf-8")
    pairs = re.findall(r'title="([^"]*)",\s*author="([^"]*)"', cli)
    out_dir = ROOT / "static" / "img" / "covers"
    out_dir.mkdir(parents=True, exist_ok=True)

    for title, author in pairs:
        slug = slug_for_title(title)
        h = int(hashlib.md5(title.encode("utf-8")).hexdigest(), 16)
        c1, c2 = PALETTES[h % len(PALETTES)]
        a_esc = escape_text(author)
        # Wrap long titles: split to max ~22 chars per line (rough)
        words = title.split()
        lines: list[str] = []
        cur = ""
        for w in words:
            if len(cur) + len(w) + 1 > 26:
                if cur:
                    lines.append(cur)
                cur = w
            else:
                cur = f"{cur} {w}".strip()
        if cur:
            lines.append(cur)
        lines = lines[:4]  # max 4 lines on cover
        tspans = ""
        y0 = 95
        for i, ln in enumerate(lines):
            tspans += (
                f'<tspan x="120" y="{y0 + i * 26}" text-anchor="middle" '
                f'fill="#f4f7ff" font-family="ui-sans-serif,system-ui,sans-serif" '
                f'font-size="17" font-weight="700">{escape_text(ln)}</tspan>'
            )

        svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 240 360" width="240" height="360">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="{c1}"/>
      <stop offset="100%" stop-color="{c2}"/>
    </linearGradient>
  </defs>
  <rect width="240" height="360" fill="url(#bg)"/>
  <rect x="10" y="10" width="220" height="340" rx="8" fill="none" stroke="rgba(255,255,255,0.2)" stroke-width="2"/>
  <text xml:space="preserve" font-family="ui-sans-serif,system-ui,sans-serif">
    {tspans}
  </text>
  <text x="120" y="300" text-anchor="middle" fill="rgba(244,247,255,0.82)" font-family="ui-sans-serif,system-ui,sans-serif" font-size="13">{a_esc}</text>
  <text x="120" y="332" text-anchor="middle" fill="rgba(244,247,255,0.45)" font-size="10">bookly</text>
</svg>
"""
        (out_dir / f"{slug}.svg").write_text(svg, encoding="utf-8")

    print(f"Wrote {len(pairs)} SVG covers to {out_dir.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
