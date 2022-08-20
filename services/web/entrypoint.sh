#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
        sleep 0.1
    done

    echo "postgres started!"
fi

python manage.py create_db

exec "$@"