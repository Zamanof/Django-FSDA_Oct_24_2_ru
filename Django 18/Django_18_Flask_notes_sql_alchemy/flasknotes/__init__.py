import os

from flask import Flask

from flasknotes.extensions import db, csrf
from flasknotes.config import Config


def create_app(test_config:dict|None=None)->Flask:
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(Config)
    if test_config:
        app.config.update(test_config)

    if not app.config.get('SECRET_KEY'):
        raise RuntimeError('SECRET_KEY not set')

    os.makedirs(app.instance_path, exist_ok=True)
    db.init_app(app)
    csrf.init_app(app)

    from flasknotes import api, cli, models, notes
    app.register_blueprint(api.bp, url_prefix='/api')
    app.register_blueprint(notes.bp)
    csrf.exempt(api.bp)
    app.cli.add_command(cli.init_db_command)
    return app

