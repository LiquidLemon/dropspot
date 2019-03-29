from flask import Flask
from dropspot import auth, drop


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile("../config.py", silent=True)
    app.register_blueprint(auth.bp)
    app.register_blueprint(drop.bp)
    return app


if __name__ == "__main__":
    app = create_app()
    app.run()
