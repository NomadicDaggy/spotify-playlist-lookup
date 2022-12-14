from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo
from app.models import User


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember_me = BooleanField("Remember Me")
    submit = SubmitField("Sign In")


class RegistrationForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    password2 = PasswordField(
        "Repeat Password", validators=[DataRequired(), EqualTo("password")]
    )
    submit = SubmitField("Register")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError("Please use a different username.")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError("Please use a different email address.")


class PlaylistInputForm(FlaskForm):
    # TODO: add validation for comma-separation and length of each id.
    playlist_ids = TextAreaField(
        "Spotify playlist ids, comma separated",
        validators=[DataRequired()],
        render_kw={"placeholder": "Comma separated Spotify playlist IDs"},
    )
    submit = SubmitField("Import")


class PlaylistSearchForm(FlaskForm):
    track_name = StringField("By exact track name: ")
    track_link = TextAreaField(
        "By Spotify track link: ",
        render_kw={"placeholder": "Drag song from Spotify client / Paste link"},
    )
    submit = SubmitField("Search")
