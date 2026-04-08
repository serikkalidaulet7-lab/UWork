#!/bin/sh
set -e

echo "Starting Django entrypoint..."

if [ -n "$SQLITE_PATH" ]; then
echo "Ensuring SQLite directory exists at $(dirname "$SQLITE_PATH")"
mkdir -p "$(dirname "$SQLITE_PATH")"
fi

echo "Running database migrations..."
python manage.py migrate --noinput
echo "Collecting static files..."
python manage.py collectstatic --noinput

if [ -n "$DJANGO_SUPERUSER_PASSWORD" ]; then
echo "Ensuring Django superuser exists..."
python manage.py shell -c "
import os
from django.contrib.auth import get_user_model
User = get_user_model()
username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin').strip() or 'admin'
password = os.environ['DJANGO_SUPERUSER_PASSWORD']
email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@example.com').strip() or 'admin@example.com'

user = User.objects.filter(username=username).first()
if user is None and email:
    user = User.objects.filter(email=email).first()

if user is None:
    user = User(username=username)

user.username = username
user.email = email
user.is_staff = True
user.is_superuser = True
user.set_password(password)
user.save()
print(f'superuser ready: {username}')
"
fi

echo "Launching application on port ${PORT:-8000}..."
exec "$@"
