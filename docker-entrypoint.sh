# This will make sure Postgres is available or running migrate during container start-up
# (a) make sure a database is available (usually only needed when used with Docker Compose)
# (b) run outstanding migrations, if any, if the DJANGO_MANAGEPY_MIGRATE is set to on in your environment.

#!/bin/sh
set -e

until psql $DATABASE_URL -c '\l'; do
    >&2 echo "Postgres is unavailable - sleeping"
    sleep 1
done

>&2 echo "Postgres is up - continuing"

if [ "x$DJANGO_MANAGEPY_MIGRATE" = 'xon' ]; then
    /venv/bin/python manage.py migrate --noinput
fi

exec "$@"