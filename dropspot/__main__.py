from flask import Flask
from dropspot import auth, drop


def create_app():
    app = Flask(__name__)
    app.register_blueprint(drop.bp)
    return app


if __name__ == "__main__":
    app = create_app()
    app.run()
