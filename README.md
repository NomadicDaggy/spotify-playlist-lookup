# Spotify playlist lookup

Service, that allows lookup of Spotify playlists by songs that they contain. 

Site NOT available at https://dags.dev

Upstream: https://github.com/NomadicDaggy/flask-on-docker

## Usage

Requires docker and docker-compose

For running the development version see `dev_run.sh`

For production deployment use `prod_run.sh`, but that also requires `.env.prod` and `.env.prod.db` to be created and filled

For testing, run from test_run.sh

The app is visible at localhost:1337

You can connect to the database with `sudo docker-compose exec db psql --username=hello_flask --dbname=hello_flask_dev`

And see server logs with `docker-compose logs -f`

New migration from `services/web` folder with `flask db migrate -m "reason for migration"`

## Big stuff missing

* Async
* Logs
* Comprehensive tests

