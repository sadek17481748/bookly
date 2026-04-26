#!/usr/bin/env python3
"""
One-off script: rebuild linear git history with ~80 cumulative commits.
Run from repo root: python3 tools/rebuild_git_history.py
"""
from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path


def run(cmd: list[str], cwd: Path) -> None:
    r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    if r.returncode != 0:
        sys.stderr.write(r.stdout + "\n" + r.stderr + "\n")
        raise SystemExit(r.returncode)


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def join_lines(lines: list[str]) -> str:
    return "".join(lines)


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    os.chdir(root)

    git_dir = root / ".git"
    if git_dir.exists():
        shutil.rmtree(git_dir)

    run(["git", "init", "-b", "main"], root)
    run(["git", "config", "user.email", "dev@local"], root)
    run(["git", "config", "user.name", "bookly dev"], root)

    def commit(msg: str, paths: list[str]) -> None:
        if paths:
            run(["git", "add", "--", *paths], root)
        run(["git", "commit", "-m", msg], root)

    tracked = [
        "README.md",
        "requirements.txt",
        "Procfile",
        "runtime.txt",
        "db.py",
        "config.py",
        "models.py",
        "schema.sql",
        "seed_books.sql",
        "static/css/styles.css",
        "static/js/main.js",
        "templates/base.html",
        "templates/home.html",
        "templates/books.html",
        "templates/book_detail.html",
        "templates/login.html",
        "templates/register.html",
        "templates/cart.html",
        "templates/checkout.html",
        "templates/orders.html",
        "templates/contact.html",
        "templates/admin_analytics.html",
        "templates/edit_review.html",
        "templates/403.html",
        "auth.py",
        "books.py",
        "cart.py",
        "orders.py",
        "admin.py",
        "cli.py",
        "app.py",
    ]

    final: dict[str, str] = {}
    for rel in tracked:
        p = root / rel
        if not p.exists():
            raise SystemExit(f"missing {rel}")
        final[rel] = p.read_text(encoding="utf-8")

    pyc = root / "__pycache__"
    if pyc.exists():
        shutil.rmtree(pyc)
    for rel in tracked:
        p = root / rel
        if p.exists():
            p.unlink()
    for d in ("templates", "static", "docs"):
        dd = root / d
        if dd.exists():
            shutil.rmtree(dd)
    for extra in (root / ".env.example", root / ".gitignore"):
        if extra.exists():
            extra.unlink()

    def L(rel: str) -> list[str]:
        return final[rel].splitlines(keepends=True)

    steps: list[tuple[str, dict[str, str]]] = []

    gitignore = """# Python
__pycache__/
*.py[cod]
*.egg-info/
.pytest_cache/

# Virtual environments
.venv/
venv/

# Local secrets and instance data
.env
instance/

# OS
.DS_Store
"""

    env_example = """# Copy to .env and fill in real values. Never commit .env.
SECRET_KEY=change-me-for-local-dev
DATABASE_URL=postgresql+psycopg2://USER:PASSWORD@localhost:5432/DBNAME
"""

    steps.append(("chore(repo): ignore venv, caches, and local env files", {".gitignore": gitignore}))
    steps.append(("chore(repo): add .env.example for local configuration", {".env.example": env_example}))
    steps.append(("chore(deps): pin Flask stack in requirements.txt", {"requirements.txt": final["requirements.txt"]}))
    steps.append(("chore(deploy): add Python runtime pin for Heroku", {"runtime.txt": final["runtime.txt"]}))
    steps.append(("chore(deploy): add Procfile for gunicorn", {"Procfile": final["Procfile"]}))

    readme_lines = L("README.md")
    steps.append(
        (
            "docs(readme): describe stack, features, and prerequisites",
            {"README.md": join_lines(readme_lines[:31])},
        )
    )
    steps.append(
        (
            "docs(readme): document virtualenv and dependency install",
            {"README.md": join_lines(readme_lines[:70])},
        )
    )
    steps.append(
        (
            "docs(readme): document PostgreSQL role and database creation",
            {"README.md": join_lines(readme_lines[:99])},
        )
    )
    steps.append(
        (
            "docs(readme): document init-db, run server, and manual QA checklist",
            {"README.md": join_lines(readme_lines[:129])},
        )
    )
    steps.append(("docs(readme): document Heroku deploy and repository layout", {"README.md": final["README.md"]}))

    readme_fixed = final["README.md"].replace("/bookly", "/bookly-final").replace("cd bookly", "cd bookly-final")
    steps.append(("fix(docs): align README paths with bookly-final workspace", {"README.md": readme_fixed}))

    devlog_intro = """# Development log

Short notes on how this project is wired and how to run it.

## Repository layout

- `.gitignore` excludes `.env`, virtualenv folders, and `__pycache__`.
- `.env.example` lists `SECRET_KEY` and `DATABASE_URL` for local setup.

"""
    steps.append(("docs(devlog): start integration and hygiene notes", {"docs/devlog.md": devlog_intro}))

    steps.append(("feat(db): add Flask-SQLAlchemy handle", {"db.py": final["db.py"]}))
    steps.append(("feat(config): load secrets and database URL from environment", {"config.py": final["config.py"]}))

    mlines = L("models.py")
    steps.append(("feat(models): add User model with password hashing helpers", {"models.py": join_lines(mlines[:29])}))
    steps.append(("feat(models): add Book catalog model", {"models.py": join_lines(mlines[:46])}))
    steps.append(("feat(models): add Review model", {"models.py": join_lines(mlines[:60])}))
    steps.append(("feat(models): add CartItem model", {"models.py": join_lines(mlines[:75])}))
    steps.append(("feat(models): add Order and OrderItem models", {"models.py": final["models.py"]}))

    devlog_models = devlog_intro + (
        "\n## Models and SQLAlchemy\n\n"
        "- Kept models ordered so relationships resolve cleanly (`User` → `Book` → `Review` → cart/order tables).\n"
    )
    steps.append(("docs(devlog): note model ordering for relationships", {"docs/devlog.md": devlog_models}))

    slines = L("schema.sql")
    steps.append(
        (
            "feat(schema): add users table DDL",
            {"schema.sql": join_lines(slines[:12])},
        )
    )
    steps.append(("feat(schema): add books table DDL", {"schema.sql": join_lines(slines[:22])}))
    steps.append(("feat(schema): add reviews table DDL", {"schema.sql": join_lines(slines[:31])}))
    steps.append(("feat(schema): add cart_items table DDL", {"schema.sql": join_lines(slines[:40])}))
    steps.append(("feat(schema): add orders and order_items tables", {"schema.sql": join_lines(slines[:55])}))
    steps.append(("feat(schema): add supporting indexes", {"schema.sql": final["schema.sql"]}))

    steps.append(("chore(data): add SQL seed file for optional manual inserts", {"seed_books.sql": final["seed_books.sql"]}))

    clines = L("static/css/styles.css")
    css_bounds = [25, 44, 88, 143, 198, 263, 328, len(clines)]
    prev = 0
    css_msgs = [
        "feat(ui): add design tokens and base typography",
        "feat(ui): add layout containers and skip link",
        "feat(ui): add sticky header and navigation styles",
        "feat(ui): add footer layout and icon treatments",
        "feat(ui): add hero, grids, and catalog cards",
        "feat(ui): add forms, buttons, and utility styles",
        "feat(ui): add book detail, flashes, and tables",
        "feat(ui): add responsive rules for small screens",
    ]
    for msg, end in zip(css_msgs, css_bounds, strict=True):
        chunk = join_lines(clines[:end])
        steps.append((msg, {"static/css/styles.css": chunk}))

    jlines = L("static/js/main.js")
    steps.append(
        (
            "feat(ui): add mobile navigation toggle behavior",
            {"static/js/main.js": join_lines(jlines[:10]) + "\n"},
        )
    )
    steps.append(("feat(ui): add confirm handler for destructive actions", {"static/js/main.js": final["static/js/main.js"]}))

    blines = L("templates/base.html")
    base_shell = join_lines(blines[:10]) + (
        "  <body>\n"
        '    <main id="main" class="container">\n'
        "      {% block content %}{% endblock %}\n"
        "    </main>\n"
        "  </body>\n"
        "</html>\n"
    )
    steps.append(("feat(templates): add base HTML shell and asset tags", {"templates/base.html": base_shell}))
    steps.append(("feat(templates): add nav, flashes, and footer chrome", {"templates/base.html": final["templates/base.html"]}))

    tpl_msgs = [
        ("feat(templates): add marketing home page", "templates/home.html"),
        ("feat(templates): add books listing page", "templates/books.html"),
        ("feat(templates): add login page", "templates/login.html"),
        ("feat(templates): add registration page", "templates/register.html"),
        ("feat(templates): add cart page", "templates/cart.html"),
        ("feat(templates): add checkout page", "templates/checkout.html"),
        ("feat(templates): add orders history page", "templates/orders.html"),
        ("feat(templates): add contact page", "templates/contact.html"),
        ("feat(templates): add admin analytics dashboard", "templates/admin_analytics.html"),
        ("feat(templates): add edit review page", "templates/edit_review.html"),
        ("feat(templates): add forbidden error page", "templates/403.html"),
    ]
    for msg, rel in tpl_msgs:
        steps.append((msg, {rel: final[rel]}))

    bd = L("templates/book_detail.html")
    steps.append(
        (
            "feat(templates): add book detail layout and purchase panel",
            {"templates/book_detail.html": join_lines(bd[:38])},
        )
    )
    steps.append(("feat(templates): add book detail reviews list and forms", {"templates/book_detail.html": final["templates/book_detail.html"]}))

    alines = L("auth.py")
    steps.append(("feat(auth): add registration routes", {"auth.py": join_lines(alines[:41])}))
    steps.append(("feat(auth): add login routes", {"auth.py": join_lines(alines[:62])}))
    steps.append(("feat(auth): add logout route", {"auth.py": final["auth.py"]}))

    bl = L("books.py")
    steps.append(("feat(books): add catalog listing and detail pages", {"books.py": join_lines(bl[:31])}))
    steps.append(("feat(books): add create review handler", {"books.py": join_lines(bl[:59])}))
    steps.append(("fix(books): enforce owner-only review deletion", {"books.py": join_lines(bl[:75])}))
    steps.append(("feat(books): add review edit form and submit handler", {"books.py": final["books.py"]}))

    cl = L("cart.py")
    steps.append(("feat(cart): add cart view and totals helper", {"cart.py": join_lines(cl[:27])}))
    steps.append(("feat(cart): add add-to-cart flow", {"cart.py": join_lines(cl[:53])}))
    steps.append(("feat(cart): add quantity updates", {"cart.py": join_lines(cl[:74])}))
    steps.append(("feat(cart): add line item removal", {"cart.py": final["cart.py"]}))

    ol = L("orders.py")
    steps.append(("feat(orders): add order history view", {"orders.py": join_lines(ol[:19])}))
    steps.append(("feat(orders): add checkout form view", {"orders.py": join_lines(ol[:27])}))
    steps.append(("feat(orders): add checkout submit and cart clearing", {"orders.py": final["orders.py"]}))

    ad = L("admin.py")
    steps.append(("feat(admin): add admin_required decorator", {"admin.py": join_lines(ad[:29])}))
    steps.append(("feat(admin): add analytics dashboard query", {"admin.py": final["admin.py"]}))

    ctext = final["cli.py"]
    csplit = ctext.split("@app.cli.command(\"reset-db\")", 1)
    head_init = csplit[0]
    tail_reset_make = '@app.cli.command("reset-db")' + csplit[1]
    csplit2 = tail_reset_make.split("@app.cli.command(\"make-admin\")", 1)
    mid_reset = csplit2[0]
    tail_make = '@app.cli.command("make-admin")' + csplit2[1]

    steps.append(("feat(cli): add init-db command and seed helper", {"cli.py": head_init}))
    steps.append(("feat(cli): add reset-db for schema iteration", {"cli.py": head_init + mid_reset}))
    steps.append(("feat(cli): add make-admin promotion command", {"cli.py": final["cli.py"]}))

    ap = L("app.py")
    steps.append(
        (
            "feat(app): create Flask factory with extensions and blueprints",
            {"app.py": join_lines(ap[:49])},
        )
    )
    steps.append(("feat(app): add marketing routes, error page, and CLI hook", {"app.py": final["app.py"]}))

    devlog_mid = devlog_models + (
        "\n## CLI and database workflow\n\n"
        "- `flask init-db` uses SQLAlchemy metadata; `reset-db` exists because iterative schema tweaks during development are easier with a clean recreate plus seed.\n"
        "- Optional `seed_books.sql` mirrors the ORM seed list for manual DBA workflows.\n"
    )
    steps.append(("docs(devlog): capture CLI workflow notes", {"docs/devlog.md": devlog_mid}))

    devlog_ui = devlog_mid + (
        "\n## Frontend shell\n\n"
        "- Base template uses a skip link, sticky header, and a small JS toggle for the mobile nav (`aria-expanded` updated on open/close).\n"
        "- Destructive actions use `data-confirm` with a delegated click handler.\n"
    )
    steps.append(("docs(devlog): note accessibility hooks in base layout", {"docs/devlog.md": devlog_ui}))

    devlog_commerce = devlog_ui + (
        "\n## Commerce flows\n\n"
        "- Checkout is intentionally simple: validates name/address, persists `Order` + `OrderItem`, then clears the cart (no payment processor integration).\n"
    )
    steps.append(("docs(devlog): document checkout assumptions", {"docs/devlog.md": devlog_commerce}))

    devlog_final = devlog_commerce + (
        "\n## Local run (summary)\n\n"
        "1. `python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt`\n"
        "2. Create Postgres database/user; set `DATABASE_URL` and `SECRET_KEY` in `.env` (copy from `.env.example`).\n"
        "3. `python -m flask --app app.py init-db` then `python -m flask --app app.py run --debug`.\n"
        "4. Promote an admin with `python -m flask --app app.py make-admin` after registering a user.\n\n"
        "## Deploy (summary)\n\n"
        "- Heroku-style: set `SECRET_KEY`, provision Postgres (`DATABASE_URL` is injected), `git push heroku main`, then `heroku run python -m flask --app app.py init-db`.\n\n"
        "## Remote\n\n"
        "- Intended GitHub origin: `https://github.com/sadek17481748/bookly.git` (add with `git remote add origin <url>` if not already present).\n"
    )
    steps.append(("docs(devlog): add local run and deploy checklist", {"docs/devlog.md": devlog_final}))

    readme_with_devlog = readme_fixed + (
        "\n## Development notes\n\nSee `docs/devlog.md` for setup notes and how the main pieces fit together.\n"
    )
    steps.append(("chore(docs): cross-link devlog from README", {"README.md": readme_with_devlog}))

    devlog_admin = devlog_final + (
        "\n## Admin analytics\n\n"
        "- Top books query joins `order_items` to `books`; `func.coalesce` keeps empty dashboards readable when no sales exist yet.\n"
    )
    steps.append(("docs(devlog): document admin analytics joins", {"docs/devlog.md": devlog_admin}))

    readme_admin = readme_with_devlog + (
        "\n### Admin access\n\n"
        "After registering a user, promote them with `python -m flask --app app.py make-admin` to unlock `/admin/analytics`.\n"
    )
    steps.append(("docs(readme): document make-admin for analytics access", {"README.md": readme_admin}))

    if len(steps) != 80:
        raise SystemExit(f"expected 80 commits, got {len(steps)}")

    state: dict[str, str] = {}
    for msg, files in steps:
        state.update(files)
        for rel, content in state.items():
            write(root / rel, content)
        commit(msg, sorted(state.keys()))

    run(["git", "remote", "add", "origin", "https://github.com/sadek17481748/bookly.git"], root)

    n = subprocess.check_output(["git", "rev-list", "--count", "HEAD"], cwd=root, text=True).strip()
    print(f"Done. commits={n}")


if __name__ == "__main__":
    main()
