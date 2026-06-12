#!/bin/sh
set -e

python manage.py migrate --noinput

if [ "${IMPORT_LEGACY_SQLITE:-false}" = "true" ]; then
    python manage.py import_legacy_sqlite
fi

python manage.py collectstatic --noinput

exec "$@"
