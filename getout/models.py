# -*- coding: utf-8 -*-

from __future__ import division, print_function

__all__ = ["db", "login_manager", "User", "Location", "Visit"]

from flask.ext import login
from flask.ext.sqlalchemy import SQLAlchemy

from werkzeug.security import (generate_password_hash, check_password_hash,
                               gen_salt)

db = SQLAlchemy()
login_manager = login.LoginManager()
login_manager.login_view = "auth.login"


class User(db.Model, login.UserMixin):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)

    # Hashed password and username.
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)

    # Account creation.
    confirmation_code = db.Column(db.String(12))
    confirmation_expiry = db.Column(db.DateTime)
    confirmed = db.Column(db.Boolean, default=False)

    # Password reset.
    reset_code = db.Column(db.String(64))
    reset_expiry = db.Column(db.DateTime)

    # User information.
    given_name = db.Column(db.Text)
    family_name = db.Column(db.Text)
    picture = db.Column(db.Text)
    bio = db.Column(db.Text)
    location = db.Column(db.Text)

    # Stats.
    last_login_at = db.Column(db.DateTime)
    last_login_ip = db.Column(db.Text)
    login_count = db.Column(db.Integer, default=0)

    def __init__(self, username, email, password):
        self.username = username
        self.set_email(email)
        self.set_password(password)

        self.confirmation_code = gen_salt(12)

    def set_email(self, em):
        self.email = generate_password_hash(em)

    def check_email(self, em):
        return check_password_hash(self.email, em)

    def set_password(self, pw):
        self.password = generate_password_hash(pw)

    def check_password(self, pw):
        return check_password_hash(self.password, pw)


class Space(db.Model):

    __tablename__ = "spaces"

    id = db.Column(db.Integer, primary_key=True)
    uniquename = db.Column(db.Text, unique=True)
    name = db.Column(db.Text)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)


class Visit(db.Model):

    __tablename__ = "visits"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    user = db.relationship(User, backref=db.backref("visits", lazy="dynamic"))
    space_id = db.Column(db.Integer, db.ForeignKey("spaces.id"))
    space = db.relationship(Space, backref=db.backref("visits",
                                                      lazy="dynamic"))
