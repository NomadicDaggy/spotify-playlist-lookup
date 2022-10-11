import os
import logging
from flask import Flask
from flask_cors import CORS

from extensions import db, migrate, celery, cache, limiter
from app.api import api


logging.basicConfig(
    level=logging.DEBUG,
    format="[%(asctime)s]: {} %(levelname)s %(message)s".format(os.getpid()),
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[logging.StreamHandler()],
)


def create_app():
    app = Flask(__name__)
    env = os.getenv("FLASK_ENV")

    confname = (
        "app.config.Config" if env == "development" else "app.config.ProductionConfig"
    )

    app.config.from_object(confname)
    app.secret_key = app.config["SECRET_KEY"]

    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})  # noqa: F841

    db.init_app(app)
    migrate.init_app(app, db)
    init_celery(app)
    cache.init_app(app)
    limiter.init_app(app)

    api.init_app(app)

    from app.routes import route_blueprint, login_manager

    app.register_blueprint(route_blueprint)

    login_manager.init_app(app)

    login_manager.blueprint_login_views = {
        "route_blueprint": "/login",
    }

    @app.shell_context_processor
    def shell_context():
        return {"app": app, "db": db}

    app.app_context().push
    return app


def init_celery(app=None):
    app = app or create_app()
    celery.conf.update(app.config.get("CELERY", {}))

    class ContextTask(celery.Task):
        """Make celery tasks work with Flask app context"""

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery
