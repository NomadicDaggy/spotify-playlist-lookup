from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


app = Flask(__name__)
app.config.from_object("app.config.Config")
app.secret_key = app.config["SECRET_KEY"]
db = SQLAlchemy(app)
login = LoginManager(app)
login.login_view = "login"
