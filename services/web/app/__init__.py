from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate


def create_app():
    app = Flask(__name__)
    app.config.from_object("app.config.Config")
    app.secret_key = app.config["SECRET_KEY"]

    from app.models import db, User

    db.init_app(app)
    migrate = Migrate(app, db)

    from app.routes import route_blueprint

    app.register_blueprint(route_blueprint)

    login = LoginManager(app)
    login.login_view = "login"

    @login.user_loader
    def load_user(id):
        return User.query.get(int(id))

    @app.shell_context_processor
    def shell_context():
        return {"app": app, "db": db}

    return app
