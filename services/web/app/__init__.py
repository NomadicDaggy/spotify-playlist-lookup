import os
import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from flask_migrate import Migrate


logging.basicConfig(
    level=logging.DEBUG,
    format="[%(asctime)s]: {} %(levelname)s %(message)s".format(os.getpid()),
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[logging.StreamHandler()],
)

db = SQLAlchemy()
migrate = Migrate()


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

    from app.routes import route_blueprint, login_manager

    app.register_blueprint(route_blueprint)

    login_manager.init_app(app)

    @app.shell_context_processor
    def shell_context():
        return {"app": app, "db": db}

    return app
