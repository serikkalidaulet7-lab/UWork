# Deploy with Docker Compose

## 1. Start the app

```bash
docker compose up --build -d
```

The site will be available on port `8000`.

## 2. Open it

```text
http://localhost:8000
http://localhost:8000/admin/
```

## 3. Important environment values

Edit `docker-compose.yml` before public deployment:

- `DJANGO_SECRET_KEY`
- `DJANGO_ALLOWED_HOSTS`
- `DJANGO_DEBUG`

## 4. Useful commands

```bash
docker compose logs -f
docker compose down
docker compose exec web python manage.py createsuperuser
```

# Deploy on Railway

This repository is deployed from the repo root.

## 1. Create the service

- In Railway, create a service from the GitHub repository.
- Railway will detect the root `Dockerfile` automatically.

## 2. Set required variables

- `DJANGO_SECRET_KEY`
- `DJANGO_ALLOWED_HOSTS`
- `DJANGO_DEBUG=False`
- Optional for persistent SQLite path: `SQLITE_PATH=/app/data/db.sqlite3`

If you want the admin user to be created automatically, also set:

- `DJANGO_SUPERUSER_USERNAME`
- `DJANGO_SUPERUSER_PASSWORD`
- `DJANGO_SUPERUSER_EMAIL`

## 3. Persistent storage

If you keep SQLite in production, attach a Railway Volume and mount it to `/app/data`.

Without a volume, SQLite data will be lost on redeploy.
