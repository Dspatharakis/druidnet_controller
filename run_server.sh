#!/bin/bash

if [ "$DATABASE" = "postgres" ]
then
  echo "Waiting for postgres..."

  while ! nc -z $SQL_HOST $SQL_PORT; do
    sleep 0.1
  done

  echo "PostgreSQL started"

fi
sleep 1

set -m
python manage.py run -h 0.0.0.0 --no-debugger --with-threads &
python manage.py create_db 
python manage.py seed_db 
echo 'Druidnet Controller is Ready!'
fg %1
exec "$@"