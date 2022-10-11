from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_caching import Cache
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from celery import Celery

# singletons for import in app factory
db = SQLAlchemy()
migrate = Migrate()
celery = Celery()

cache = Cache(config={"CACHE_TYPE": "SimpleCache"})

limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["600 per hour", "1 per second"],
    storage_uri="memory://",
)
