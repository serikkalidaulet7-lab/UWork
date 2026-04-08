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

if [ -n "$DJANGO_SUPERUSER_USERNAME" ] && [ -n "$DJANGO_SUPERUSER_PASSWORD" ]; then
echo "Ensuring Django superuser exists..."
python manage.py shell -c "
import os
from django.contrib.auth import get_user_model
User = get_user_model()
username = os.environ['DJANGO_SUPERUSER_USERNAME']
password = os.environ['DJANGO_SUPERUSER_PASSWORD']
email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@example.com')
user, created = User.objects.get_or_create(username=username, defaults={'email': email, 'is_staff': True, 'is_superuser': True})
user.email = email
user.is_staff = True
user.is_superuser = True
user.set_password(password)
user.save()
print('superuser ready')
"
fi

echo "Launching application on port ${PORT:-8000}..."
exec "$@"
