from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
# from flask_sqlalchemy import SQLAlchemy


class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    psw = db.Column(db.String(500), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return "<{}:{}>".format(self.id, self.username)

        def set_password(self, password):
            self.psw = generate_password_hash(password)

        def check_password(self, password):
            return check_password_hash(self.psw, password)


class Events(db.Model):
    __tablename__ = "events"
    _id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(50), nullable=False)
    begin = db.Column(db.Date, unique=False, nullable=False)
    end = db.Column(db.Date, unique=False, nullable=False)
    topic = db.Column(db.String(80), unique=False, nullable=False)
    description = db.Column(db.Text, unique=False, nullable=False)
