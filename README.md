# bookly — bookstore (PostgreSQL + HTML + CSS + JavaScript + Python)

## Table of Contents

- [Overview](#overview)
  - [Project goals](#project-goals)
  - [Planning notes (written at project start)](#planning-notes-written-at-project-start)
- [Quick links](#quick-links)
  - [Marking criteria → README (assessor map)](#marking-criteria--readme-assessor-map)
- [Key UI screenshots](#key-ui-screenshots)
- [Features](#features)
- [User Experience (UX)](#user-experience-ux)
  - [Responsive behaviour](#responsive-behaviour)
  - [How responsiveness was tested](#how-responsiveness-was-tested)
  - [User stories](#user-stories)
- [Wireframes](#wireframes)
- [Design](#design)
  - [Data model and ERD (entity relationships)](#data-model-and-erd-entity-relationships)
- [Technologies Used](#technologies-used)
- [File Structure](#file-structure)
- [Development](#development)
- [Deployment](#deployment)
- [Technical overview](#technical-overview)
  - [Why PostgreSQL is the technical centre of this work](#why-postgresql-is-the-technical-centre-of-this-work)
  - [Request flow overview](#request-flow-overview)
  - [Role of Flask](#role-of-flask)
  - [Project 3 scope vs what this submission demonstrates](#project-3-scope-vs-what-this-submission-demonstrates)
  - [Database (PostgreSQL)](#database-postgresql)
  - [HTML, CSS, JavaScript](#html-css-javascript)
- [Testing and Bugs](#testing-and-bugs)
  - [Assessment test matrix (functionality, usability, responsiveness, data management)](#assessment-test-matrix-functionality-usability-responsiveness-data-management)
  - [Manual Testing](#manual-testing)
  - [Automated Testing](#automated-testing)
  - [Feature to test mapping](#feature-to-test-mapping)
  - [Running pytest locally (terminal evidence)](#running-pytest-locally-terminal-evidence)
  - [Testing summary table](#testing-summary-table)
  - [Bugs encountered during development](#bugs-encountered-during-development)
  - [Use of AI (assistance log)](#use-of-ai-assistance-log)
  - [Lighthouse Testing](#lighthouse-testing)
  - [HTML, CSS and JS Validation](#html-css-and-js-validation)
- [Sources and references](#sources-and-references)
  - [Feature resources (inspiration & references)](#feature-resources-inspiration--references)
  - [Flask](#flask)
  - [PostgreSQL (5 videos)](#postgresql-5-videos)
  - [Python (15 videos / playlists)](#python-15-videos--playlists)
  - [Sources for Python](#sources-for-python)
  - [Images used in this project](#images-used-in-this-project)
  - [Image credits](#image-credits)
- [Attributions](#attributions)
- [Additional Notes](#additional-notes)
- [Author](#author)

---

## Quick links

Assessor-facing links and evidence paths (also useful when marking without searching the whole README):

| Resource | Link or path |
|----------|----------------|
| **Source repository** | `https://github.com/sadek17481748/bookly` — application code and this `README.md` |
| **Live deployment (Heroku)** | `https://bookly-final-98e88d5d388e.herokuapp.com/` |
| **Wireframes (PDF)** | [`docs/wireframe-bookly.pdf`](docs/wireframe-bookly.pdf) |
| **Wireframes (README anchor)** | [Wireframes](#wireframes) |
| **Live app login page** | `/login` on the Heroku URL above |
| **Analytics dashboard (admin-only)** | `/admin/analytics` — KPIs and tables (requires an admin account) |
| **Assessor admin login (example)** | `analytics@testemail.com` / `test123` — see [Development](#development) if the account must be registered on the live database first |
| **Bug tracker (GitHub Project board)** | `https://github.com/users/sadek17481748/projects/6` |
| **GitHub Pages (documentation site)** | `https://sadek17481748.github.io/bookly` |
| **Closed issues (progress log)** | GitHub **Issues** (closed) on the repository |
| **Bug / fix narratives** | [`docs/fix-log.md`](docs/fix-log.md) — short notes per fix next to the manual checklist |
| **Manual test evidence (screenshots)** | [`docs/images/manual-testing/`](docs/images/manual-testing/) — filenames match the [Manual testing](#manual-testing) table |
| **Validation tooling evidence** | [`docs/images/validation/`](docs/images/validation/) — Lighthouse, W3C validators, JSHint, 404, responsiveness composite |

Key screens are also embedded under [Key UI screenshots](#key-ui-screenshots) below.

### Marking criteria → README (assessor map)

These rows tie **this `README.md` only** (no extra marker document) to the parts of the brief that ask for **database design**, **testing across the full stack**, and **a project data model**. The evidence named here is what you should scroll to in the sections linked.

| Criterion (brief wording) | What you should see in this README | Anchor |
|---------------------------|-------------------------------------|--------|
| **Domain database design** — structure relevant to the domain **and relationships between entities** | Relational entities (users, books, reviews, cart, orders), **cardinality table**, and a **Mermaid ERD** showing keys and links between tables. Same design is reflected in `models.py` and `schema.sql`. | [Data model and ERD (entity relationships)](#data-model-and-erd-entity-relationships) |
| **1.5** — test procedures for **functionality**, **usability**, **responsiveness**, and **data management** in the full-stack app | The **four-row assessment matrix** (what was tested, how, where to read it), then the **numbered manual checklist** with Pass/Fail and screenshot paths, plus **automated testing** and the **testing summary** table. | [Assessment test matrix](#assessment-test-matrix-functionality-usability-responsiveness-data-management); [Manual testing](#manual-testing); [Automated testing](#automated-testing); [Testing summary table](#testing-summary-table) |
| **2.1** — **data model** that fits the project purpose | Same subsection as the first row: the ERD and narrative explain how the schema supports browsing, reviews, cart, checkout, and admin reporting. | [Data model and ERD (entity relationships)](#data-model-and-erd-entity-relationships) |

---

