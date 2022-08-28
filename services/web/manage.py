from flask.cli import FlaskGroup

from app.models import User, db
from app import create_app


cli = FlaskGroup(create_app=create_app)


@cli.command("create_db")
def create_db():
    db.drop_all()
    db.create_all()
    db.session.commit()


@cli.command("seed_db")
def seed_db():
    user = User(
        email="example@gmail.com",
        username="admin",
    )
    user.set_password("admin")
    db.session.add(user)
    db.session.commit()


if __name__ == "__main__":
    cli()
