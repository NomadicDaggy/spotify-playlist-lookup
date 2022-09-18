from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from celery import Celery
from flask_restful import Api

# singletons for import in app factory
db = SQLAlchemy()
migrate = Migrate()
celery = Celery()
api = Api()
