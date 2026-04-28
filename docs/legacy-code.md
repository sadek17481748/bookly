# Legacy code snapshots (before improvements)

This file preserves **small excerpts** of earlier implementations that were later improved during development. It exists for coursework review so an assessor can see examples of “old code” and understand what was changed and why.

> Notes
> - These snippets are **representative excerpts**, not full files.
> - The “after” versions are present in the current codebase; the “before” versions are shown here for comparison.

---

## 1) Book cover URLs (SVG-only → prefer raster covers + SVG fallback)

### Before (SVG-only)

Problem: the project originally used only SVG placeholder covers, and the helper always returned a `.svg` path.

```python
def cover_static_url(title: str) -> str:
    """URL path served by Flask static (see static/img/covers/*.svg)."""
    return f"/static/img/covers/{slug_for_title(title)}.svg"
```

### After (prefer `.png`/`.jpg`/`.webp` when present)

Improvement: when a real cover image is available under `static/img/covers/`, the helper serves it; otherwise it falls back to the SVG placeholder.

```python
def cover_static_url(title: str) -> str:
    slug = slug_for_title(title)
    for ext in (".png", ".jpg", ".jpeg", ".webp", ".svg"):
        if (covers_dir / f"{slug}{ext}").exists():
            return f"/static/img/covers/{slug}{ext}"
    return f"/static/img/covers/{slug}.svg"
```

---

## 2) Seeding behaviour (`init-db` only seeded empty DB → backfill/upgrade existing rows)

### Before (seed only if the catalogue is empty)

Problem: if the `books` table already contained rows from an earlier seed, running `flask init-db` would **not** update missing `cover_url` values (because it returned early).

```python
def _seed_books_if_empty() -> None:
    if Book.query.count() != 0:
        return
    db.session.add_all(seed_books)
    db.session.commit()
```

### After (insert missing titles and backfill/upgrade `cover_url`)

Improvement: `init-db` now behaves more like an “upsert” for seed data:
it inserts any missing seeded titles and fixes older rows with missing/placeholder cover URLs.

```python
def _seed_books() -> None:
    for seeded in seed_books:
        existing = Book.query.filter_by(title=seeded.title).first()
        if existing is None:
            db.session.add(seeded)
            continue

        if (not existing.cover_url) or (
            existing.cover_url.endswith(".svg") and existing.cover_url != seeded.cover_url
        ):
            existing.cover_url = seeded.cover_url

    db.session.commit()
```

---

## 3) Manual testing evidence (paths were plain text → clickable links)

### Before (plain text paths)

Problem: screenshot evidence entries were listed as paths, but not clickable.

```markdown
| 1 | Public | Open `/` | Home loads |  |  | `docs/images/manual-testing/01-home.png` |
```

### After (readable link labels)

Improvement: evidence is now clickable and easier to scan.

```markdown
| 1 | Public | Open `/` | Home loads |  |  | [01-home](docs/images/manual-testing/01-home.png) |
```

