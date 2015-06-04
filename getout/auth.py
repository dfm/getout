# -*- coding: utf-8 -*-

from __future__ import division, print_function

__all__ = ["auth"]

import flask

auth = flask.Blueprint("auth", __name__)


@auth.route("/signup", methods=["GET", "POST"])
def signup():
    return flask.render_template("signup.html")


@auth.route("/login", methods=["GET", "POST"])
def login():
    return flask.render_template("login.html")


@auth.route("/profile", methods=["GET", "POST"])
def edit_profile():
    return flask.render_template("edit_profile.html")
