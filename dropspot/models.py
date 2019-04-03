from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40), index=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    otp_secret = db.Column(db.String(20))

    def __repr__(self):
        return "<User {}>".format(self.email)
