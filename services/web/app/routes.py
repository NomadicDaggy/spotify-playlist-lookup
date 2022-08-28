from flask import (
    flash,
    redirect,
    render_template,
    request,
    url_for,
    Blueprint,
)
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.urls import url_parse


from app.forms import LoginForm, RegistrationForm, PlaylistInputForm
from app.models import User, db


route_blueprint = Blueprint("route_blueprint", __name__)


@route_blueprint.route("/")
@route_blueprint.route("/index")
def index():
    return render_template("index.html", title="Home")


@route_blueprint.route("/import_playlists", methods=["GET", "POST"])
@login_required
def import_playlists():
    form = PlaylistInputForm()
    return render_template("import_playlists.html", title="Import Playlists", form=form)


@route_blueprint.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("route_blueprint.index"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("Invalid username or password")
            return redirect(url_for("route_blueprint.login"))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get("next")
        if not next_page or url_parse(next_page).netloc != "":
            next_page = url_for("route_blueprint.index")
        return redirect(next_page)
    return render_template("login.html", title="Sign In", form=form)


@route_blueprint.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("route_blueprint.index"))


@route_blueprint.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("route_blueprint.index"))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Congratulation, you are now a registered user!")
        return redirect(url_for("route_blueprint.login"))
    return render_template("register.html", title="Register", form=form)
