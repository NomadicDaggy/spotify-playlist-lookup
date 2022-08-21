# Flask on Docker

Site available at https://dags.dev

My step-through of this guide: https://github.com/testdrivenio/flask-on-docker

Adding login functionality from: https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world

SSL cert generated with letsencrypt

## Usage

Requires docker and docker-compose

For running the development version see `dev_run.sh`

For production deployment use `prod_run.sh`, but that also requires `.env.prod` and `.env.prod.db` to be created and filled

The app is visible at localhost:1337

You can connect to the database with `sudo docker-compose exec db psql --username=hello_flask --dbname=hello_flask_dev`

And see server logs with `docker-compose logs -f`
