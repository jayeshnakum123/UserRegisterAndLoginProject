from app import db, bcrypt
from sqlalchemy import Column, Integer, String
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf.file import FileField, FileAllowed


class user_signin(db.Model, UserMixin):
    __tablename__ = "credentials"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50))
    password = db.Column(db.String(50))
    email = db.Column(db.String(50), unique=True)
    mobile = db.Column(db.String(12), unique=True)
    profile_picture = db.Column(db.String(255))

    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password).decode("utf-8")

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)

    # this is the update profile mate function banavel che..
    def update_profile(self, username, email, mobile, profile_picture):
        self.username = username
        self.email = email
        self.mobile = mobile
        self.profile_picture = profile_picture
        db.session.commit()


class Auth(db.Model):
    __tablename__ = "Auth"
    # id = Column(Integer, primary_key=True)
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
