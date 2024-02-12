from app import db
from sqlalchemy import Column, Integer, String
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class user_signin(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50))
    password = db.Column(db.String(50))
    email = db.Column(db.String(50), unique=True)
    mobile = db.Column(db.String(12), unique=True)

    # def __init__(self, username, password, email, mobile):
    #     self.username = username
    #     self.password = bcrypt.hashpw(
    #         password.encode(encoding="utf-8"), bcrypt.gensalt()
    #     ).decode("utf-8")

    # def check_password(self, password):
    #     # return  bcrypt.checkpw(password.encode('utf-8'),self.password)
    #     pass


class Auth(db.Model):
    __tablename__ = "Auth"
    # id = Column(Integer, primary_key=True)
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
