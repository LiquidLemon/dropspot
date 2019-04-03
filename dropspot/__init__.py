from pathlib import Path
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dropspot import auth, drop, profile
import os

migrate = Migrate()


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile("../config.py", silent=True)
    app.register_blueprint(auth.bp)
    app.register_blueprint(drop.bp)
    app.register_blueprint(profile.bp)

    from dropspot.models import db

    db.init_app(app)

    database = Path(app.config["DATABASE_PATH"])
    if not database.is_file():
        print("no database detected, creating one")
        with app.app_context():
            db.create_all()

    migrate.init_app(app, db)

    return app
