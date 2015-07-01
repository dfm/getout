# -*- coding: utf-8 -*-

from __future__ import division, print_function

__all__ = ["db", "login_manager", "User", "Space", "Visit"]

from datetime import datetime, timedelta

from flask.ext import login
from flask.ext.sqlalchemy import SQLAlchemy

from werkzeug.security import (generate_password_hash, check_password_hash,
                               gen_salt)

db = SQLAlchemy()
login_manager = login.LoginManager()
login_manager.login_view = "auth.login"

follows = db.Table(
    "follows",
    db.Column("follower_id", db.Integer, db.ForeignKey("users.id")),
    db.Column("followee_id", db.Integer, db.ForeignKey("users.id")),
    db.UniqueConstraint("follower_id", "followee_id")
)


class User(db.Model, login.UserMixin):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)

    # Hashed password and username.
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.Text, unique=True, nullable=False)

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

    # Followers.
    following = db.relation(
        "User",
        secondary=follows,
        primaryjoin=follows.c.follower_id == id,
        secondaryjoin=follows.c.followee_id == id,
        backref="followers"
    )

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.set_password(password)

        self.confirmation_code = gen_salt(12)
        self.confirmation_expiry = datetime.now() + timedelta(days=10)

    def set_password(self, pw):
        self.password = generate_password_hash(pw)

    def check_password(self, pw):
        return check_password_hash(self.password, pw)


space_categories = db.Table(
    "space_categories",
    db.Column("space_id", db.Integer, db.ForeignKey("spaces.id")),
    db.Column("category_id", db.Integer, db.ForeignKey("categories.id"))
)


class Category(db.Model):

    __tablename__ = "categories"

    id = db.Column(db.Integer, primary_key=True)
    short_name = db.Column(db.Text, unique=True)
    name = db.Column(db.Text, unique=True)


class Space(db.Model):

    __tablename__ = "spaces"

    id = db.Column(db.Integer, primary_key=True)
    uniquename = db.Column(db.Text, unique=True)
    name = db.Column(db.Text)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    creation_date = db.Column(db.DateTime)

    owner_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    owner = db.relationship(User, backref=db.backref("spaces", lazy="dynamic"))

    parent_id = db.Column(db.Integer, db.ForeignKey("spaces.id"))
    parent = db.relationship(User, backref=db.backref("children",
                                                      lazy="dynamic"))

    categories = db.relationship(Category, secondary=space_categories,
                                 backref=db.backref("spaces", lazy="dynamic"))


class Visit(db.Model):

    __tablename__ = "visits"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    user = db.relationship(User, backref=db.backref("visits", lazy="dynamic"))
    space_id = db.Column(db.Integer, db.ForeignKey("spaces.id"))
    space = db.relationship(Space, backref=db.backref("visits",
                                                      lazy="dynamic"))
    visit_datetime = db.Column(db.DateTime)
