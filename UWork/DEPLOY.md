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
