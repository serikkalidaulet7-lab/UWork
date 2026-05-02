# Deploy with Docker Compose

## 1. Create a local env file

From the `UWork/` directory:

```bash
cp .env.example .env
```

Set a real `DJANGO_SECRET_KEY` before sharing or deploying the app anywhere public.

## 2. Start the app

```bash
docker compose up --build -d
```

The site will be available on:

```text
http://localhost:8000
http://localhost:8000/admin/
```

## 3. Useful commands

```bash
docker compose logs -f
docker compose down
docker compose exec web python manage.py createsuperuser
```

# Deploy on Railway

This repository deploys from the repo root. Railway uses the root `Dockerfile`, while the Django app itself lives under `UWork/`.

## 1. Create the service

- Create a Railway service from the GitHub repository.
- Railway will detect the root `Dockerfile`.
- The healthcheck path is `/health/`.

## 2. Set required variables

- `DJANGO_ENV=production`
- `DJANGO_SECRET_KEY`
- `DJANGO_ALLOWED_HOSTS`
- `DJANGO_DEBUG=False`
- Optional persistent SQLite path: `SQLITE_PATH=/app/data/db.sqlite3`

If you want the admin user to be created automatically, also set:

- `DJANGO_SUPERUSER_USERNAME`
- `DJANGO_SUPERUSER_PASSWORD`
- `DJANGO_SUPERUSER_EMAIL`

## 3. Persistent storage

If you keep SQLite in production, attach a Railway Volume and mount it to `/app/data`.

Without a volume, SQLite data will be lost on redeploy. The entrypoint creates the SQLite directory automatically, but storage is still ephemeral without a mounted volume.
