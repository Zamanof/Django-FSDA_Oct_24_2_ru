from flask import current_app

from flasknotes.extensions import db
from flasknotes.models import User


def get_demo_user() -> User:
    username = current_app.config["DEMO_USER"]
    user = db.session.execute(db.select(User).filter_by(username=username)).scalar_one_or_none()
    if user is None:
        raise RuntimeError("Сначала выполните: python -m flask --app flasknotes init-db")
    return user