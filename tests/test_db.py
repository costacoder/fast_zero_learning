from sqlalchemy import select

from fast_zero.models import User


def test_create_user(session):
    user = User(
        username="xand", email="xand@costa.com", password="minha-senha"
    )

    session.add(user)
    session.commit()

    result = session.scalar(select(User).where(User.email == "xand@costa.com"))

    assert result.username == "xand"
