import pytest
from app import create_app
from app.models import db


@pytest.fixture(scope="session")
def app():
    app = create_app()
    app.config.update(
        {
            "TESTING": True,
        }
    )

    with app.app_context():
        yield app


@pytest.fixture(scope="session")
def database(app):
    with app.app_context():
        db.drop_all()
        db.create_all()
        yield db


@pytest.fixture(scope="class", autouse=True)
def session(app, database, request):
    """
    Returns function-scoped session.
    """
    with app.app_context():
        conn = database.engine.connect()
        txn = conn.begin()

        options = dict(bind=conn, binds={})
        sess = database.create_scoped_session(options=options)

        database.session = sess
        yield sess

        sess.remove()
        # This instruction rollsback any commit that were executed in the tests.
        txn.rollback()
