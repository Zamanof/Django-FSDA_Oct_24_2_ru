import click
from flask import current_app
from flask.cli import with_appcontext
from werkzeug.security import generate_password_hash

from flasknotes.extensions import db
from flasknotes.models import User

@click.command('init-db')
@with_appcontext
def init_db_command():
    db.create_all()
    username = current_app.config["DEMO_USER"]
    password = current_app.config["DEMO_PASSWORD"]
    user = db.session.execute(db.select(User).filter_by(username=username)).scalar_one_or_none()
    if user is None:
        user = User(username=username, password_hash=generate_password_hash(password))
        db.session.add(user)
        db.session.commit()
        click.echo('User created')
    else:
        click.echo('User already exists')