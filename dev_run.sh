#!/bin/sh
docker-compose down -v
docker-compose up -d --build
docker-compose exec web python manage.py create_db
docker-compose exec web python manage.py seed_db
