# -*- coding: utf-8 -*-

from __future__ import division, print_function

__all__ = ["Role", "User", "Place", "Visit"]

from flask.ext import login
from flask.ext.sqlalchemy import SQLAlchemy

db = SQLAlchemy()


roles_users = db.Table(
    "roles_users",
    db.Column("user_id", db.Integer(), db.ForeignKey("users.id")),
    db.Column("role_id", db.Integer(), db.ForeignKey("roles.id"))
)


class Role(db.Model, security.RoleMixin):

    __tablename__ = "roles"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))


class User(db.Model, security.UserMixin):

    __tablename__ = "users"

    # Security columns.
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text, unique=True)
    email = db.Column(db.Text, unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean)
    confirmed_at = db.Column(db.DateTime)
    last_login_at = db.Column(db.DateTime)
    current_login_at = db.Column(db.DateTime)
    last_login_ip = db.Column(db.Text)
    current_login_ip = db.Column(db.Text)
    login_count = db.Column(db.Integer)
    roles = db.relationship("Role", secondary=roles_users,
                            backref=db.backref("users", lazy="dynamic"))

    # Other columns.
    fullname = db.Column(db.Text)
    bio = db.Column(db.Text)
    avatarurl = db.Column(db.Text)


class Place(db.Model):

    __tablename__ = "places"

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
    place_id = db.Column(db.Integer, db.ForeignKey("places.id"))
    place = db.relationship(Place,
                            backref=db.backref("visits", lazy="dynamic"))


user_datastore = security.SQLAlchemyUserDatastore(db, User, Role)
security_ext = security.Security(datastore=user_datastore)
