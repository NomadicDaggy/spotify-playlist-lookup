import os

from werkzeug.utils import secure_filename
from flask import Flask, jsonify, send_from_directory, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import (
    LoginManager,
    UserMixin,
    login_required,
    logout_user,
    current_user,
)
from flask_dance.contrib.github import make_github_blueprint, github
from flask_dance.consumer.storage.sqla import OAuthConsumerMixin, SQLAlchemyStorage


app = Flask(__name__)
app.config.from_object("project.config.Config")
app.secret_key = app.config["SECRET_KEY"]

db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(128), unique=True, nullable=False)
    active = db.Column(db.Boolean(), default=True, nullable=False)

    def __init__(self, email) -> None:
        self.email = email


@app.route("/")
def index():
    return jsonify(hello="world")


@app.route("/static/<path:filename>")
def staticfiles(filename):
    return send_from_directory(app.config["STATIC_FOLDER"], filename)


@app.route("/media/<path:filename>")
def mediafiles(filename):
    return send_from_directory(app.config["MEDIA_FOLDER"], filename)


@app.route("/upload", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        file = request.files["file"]
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config["MEDIA_FOLDER"], filename))
    return """
    <!doctype html>
    <title>upload new File</title>
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=file name=file><input type=submit value=Upload>
    </form>
    """
