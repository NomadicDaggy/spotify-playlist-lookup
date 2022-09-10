import logging
import os

from celery import Celery, current_app

from app.models import User

LOGGER = logging.getLogger()


def make_celery():
    celery = Celery(
        __name__,
        broker=os.getenv("CELERY_BROKER"),
        backend=os.getenv("CELERY_RESULT_BACKEND"),
    )

    return celery


celery = make_celery()


@celery.task
def process_data(user_id):
    LOGGER.info("Processing data")
    user = User.query.filter_by(id=user_id).first()
    user.import_all_playlists()
