import os

from flask import (
    flash,
    redirect,
    render_template,
    request,
    url_for,
    Blueprint,
    session,
)
import tekore as tk
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.urls import url_parse

from app.forms import LoginForm, RegistrationForm, PlaylistInputForm, PlaylistSearchForm
from app.models import User, db, insert_playlists_tracks, Track, Playlist
from app.api_data_import import MaterializedPlaylist


route_blueprint = Blueprint("route_blueprint", __name__)

conf = (
    os.getenv("SPOTIFY_CLIENT_ID"),
    os.getenv("SPOTIFY_CLIENT_SECRET"),
    "http://localhost:1337/spotify_callback",
)
cred = tk.Credentials(*conf)
spotify = tk.Spotify()

auths = {}


@route_blueprint.route("/")
@route_blueprint.route("/index")
def index():
    playlist_count = Playlist.query.count()
    track_count = Track.query.count()
    return render_template(
        "index.html",
        title="Home",
        playlist_count=playlist_count,
        track_count=track_count,
    )


@route_blueprint.route("/playlists", methods=["GET"])
@login_required
def playlists():
    return render_template(
        "search_playlists.html",
        title="Search Playlists",
        form=PlaylistSearchForm(),
        results="",
    )


@route_blueprint.route("/playlists", methods=["POST"])
@login_required
def search_playlists():
    form = PlaylistSearchForm()
    if form.validate_on_submit():
        if link := form.track_link.data:
            track_id = link.split("/")[-1]
            track = Track.query.filter_by(spotify_id=track_id).first()
        else:
            track = Track.query.filter_by(name=form.track_name.data).first()

        if track:
            # default
            results = "Track found, but no new playlists contain it"

            # Find playlists that contain the track
            results = track.get_playlists()
            results = [p for p in results]

        else:
            results = "Track not found, try again!"

        return render_template(
            "search_playlists.html",
            title="Search Playlists",
            form=form,
            results=results,
        )


@route_blueprint.route("/playlists/import", methods=["GET", "POST"])
@login_required
def import_playlists():
    form = PlaylistInputForm()
    if form.validate_on_submit():
        # TODO: Should this block be abstracted out to somewhere else?
        #
        # get each playlist id
        playlist_ids = form.playlist_ids.data.split(",")
        for p in playlist_ids:
            mp = MaterializedPlaylist(p)
            # get track data from spotify api
            playlist_data = mp.get_data()
            # insert into database
            insert_playlists_tracks(playlist_data)

    return render_template("import_playlists.html", title="Import Playlists", form=form)


@route_blueprint.route("/login", methods=["GET", "POST"])
def login():
    # disable for now
    return redirect(url_for("route_blueprint.index"))

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
    # disable for now
    return redirect(url_for("route_blueprint.index"))

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


@route_blueprint.route("/spotify_login", methods=["GET"])
def spotify_login():
    if current_user.is_authenticated:
        return redirect(url_for("route_blueprint.index"))

    scope = tk.scope.every
    auth = tk.UserAuth(cred, scope)
    auths[auth.state] = auth
    return redirect(auth.url, 307)


@route_blueprint.route("/spotify_callback", methods=["GET"])
def login_callback():
    code = request.args.get("code", None)
    state = request.args.get("state", None)
    auth = auths.pop(state, None)

    if auth is None:
        return "Invalid state!", 400

    token = auth.request_token(code, state)
    with spotify.token_as(token):
        u = spotify.current_user()
        print(u)

    user = User.query.filter_by(username=u.id).first()
    if user is None:
        print("creating new user")
        user = User(
            username=u.id, email="", password_hash="", active=True, generated=True
        )
        db.session.add(user)
        db.session.commit()

    login_user(user, remember=True)

    next_page = url_for("route_blueprint.index")

    return redirect(next_page)
