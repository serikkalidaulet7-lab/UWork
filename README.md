# UWork Future Ready Summit

UWork Future Ready Summit is a portfolio-focused Django project that presents a professional event microsite and attendee application flow. It combines a branded public site, structured registration form, admin-friendly reservation management, and deployment-ready configuration.

## What it showcases

- A polished multi-page marketing site with a custom responsive design
- Django models, forms, validation, and flash-message flows
- Attendee application handling with generated reference codes
- Capacity-aware waitlist logic
- Admin tooling for reviewing and updating reservation status
- Docker and Railway-friendly deployment setup

## Stack

- Python
- Django
- SQLite for local persistence
- WhiteNoise for static asset serving
- Docker for containerized local and hosted runs

## Local run

From the project root:

```bash
cd UWork
cp .env.example .env
python3 -m venv ../venv
source ../venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Open `http://127.0.0.1:8000`.

## Docker run

```bash
cd UWork
cp .env.example .env
docker compose up --build
```

## Tests

```bash
cd UWork
python manage.py test
```

## Security notes

- Local environment values belong in `UWork/.env`, which is now git-ignored.
- `db.sqlite3` is treated as local data and should not be committed.
- Exact venue details are intentionally not exposed on the public site.

## Project structure

- `UWork/base/` contains the application logic, templates, and styles
- `UWork/UWork/settings.py` holds Django configuration
- `UWork/docker-compose.yml` provides a safe local container setup
- `UWork/DEPLOY.md` documents deployment expectations
