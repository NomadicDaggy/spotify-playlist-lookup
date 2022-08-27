from app.models import User


def test_insert_user(session):
    u = User(email="test@test.com", username="tester", active=True)
    session.add(u)
    session.commit()
    assert User.query.count() == 1


def test_no_users():
    assert User.query.count() == 0
