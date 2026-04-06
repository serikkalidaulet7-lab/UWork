#!/bin/sh
set -e

if [ -n "$SQLITE_PATH" ]; then
mkdir -p "$(dirname "$SQLITE_PATH")"
fi

python manage.py migrate --noinput
python manage.py collectstatic --noinput

if [ -n "$DJANGO_SUPERUSER_USERNAME" ] && [ -n "$DJANGO_SUPERUSER_PASSWORD" ]; then
python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
username = '${DJANGO_SUPERUSER_USERNAME}'
password = '${DJANGO_SUPERUSER_PASSWORD}'
email = '${DJANGO_SUPERUSER_EMAIL:-admin@example.com}'
user, created = User.objects.get_or_create(username=username, defaults={'email': email, 'is_staff': True, 'is_superuser': True})
user.email = email
user.is_staff = True
user.is_superuser = True
user.set_password(password)
user.save()
print('superuser ready')
"
fi

exec "$@"
