#!/bin/sh
python manage.py run -h 0.0.0.0 &
python manage.py create_db &
python manage.py seed_db

exec "$@"