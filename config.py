import os

DATABASE_PATH = os.path.dirname(os.path.realpath(__file__)) + '/database.db'
UPLOAD_DIR = 'files'
SECRET_KEY = 'dev'
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + DATABASE_PATH
SQLALCHEMY_TRACK_MODIFICATIONS = False