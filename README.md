# cost-reduction-platform-demo

> This repository is a public reimplementation using synthetic data.  
> It contains no proprietary code, internal data, confidential materials, or company-specific assets.

`cost-reduction-platform-demo` is a FastAPI + SQLite portfolio demo for a cost reduction tracking workflow. It is intentionally simple, easy to run locally, and designed for recruiters, interviewers, or reviewers to understand quickly.

## What is included in V1

- Dashboard
- Cost reduction project ledger
- Create, edit, search, and filter
- CSV and Excel bulk import
- Field validation
- Duplicate detection
- Preview before confirm import
- Simple multi-factory data isolation demo
- Project detail pages
- Synthetic seed data

## What is not included

- Real company names, sites, projects, accounts, screenshots, URLs, or production data
- Proprietary code or internal business assets
- Complex authentication or RBAC
- Microservices, Docker, Kubernetes, or heavy CI/CD

## Tech stack

- Python 3.11
- FastAPI
- SQLite
- Jinja2 templates
- Tailwind via CDN

## Quick start

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Then open [http://127.0.0.1:8000](http://127.0.0.1:8000).

## Import format

Expected columns:

```text
project_code, title, factory_name, category, status, owner, estimated_savings, currency, start_date, target_date, description
```

Supported factories for the demo:

- Factory Alpha
- Factory Beta
- Factory Gamma

A synthetic example file is included at `sample_data/projects_import_template.csv`.

## Synthetic data used

The seeded demo contains only fictional examples such as:

- Factory Alpha, Factory Beta, Factory Gamma
- Compressed Air Leak Sweep
- Packaging Film Width Optimization
- Forklift Route Redesign
- Cooling Water Setpoint Review
- Returnable Pallet Expansion

All amounts, owners, and timelines are synthetic placeholders for demonstration only.

## Repository safety statement

This repository is a public reimplementation using synthetic data. It contains no proprietary code, internal data, confidential materials, or company-specific assets.
