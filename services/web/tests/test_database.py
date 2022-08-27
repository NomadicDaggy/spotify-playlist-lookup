from app.models import User


def test_db_empty():
    assert User.query.count() == 0
