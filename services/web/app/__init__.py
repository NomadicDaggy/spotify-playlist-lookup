import os
import logging
from flask import Flask

from extensions import db, migrate, celery


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

    db.init_app(app)
    migrate.init_app(app, db)
    init_celery(app)

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
