# -*- coding: utf-8 -*-

from __future__ import division, print_function

__all__ = ["auth"]

import sqlalchemy
from datetime import datetime

import flask
from flask.ext.login import (current_user, login_user, logout_user,
                             login_required)

from .models import db, login_manager, User
from .forms import SignupForm
from .email import send_confirmation

auth = flask.Blueprint("auth", __name__)


@auth.route("/google_oauth2callback")
def google_oauth2callback():
    # Check the response from Google.
    resp = google.authorized_response()
    if resp is None:
        return "Access denied: reason={0} error={1}".format(
            flask.request.args["error_reason"],
            flask.request.args["error_description"]
        )
    elif isinstance(resp, OAuthException):
        return flask.abort(404)

    # Save the token to the session and get the user info.
    flask.session["google_token"] = resp["access_token"]
    me = google.get("userinfo").data

    # Save or update the user in the database.
    user = User.query.filter_by(google_id=me["id"]).first()
    if user is None:
        user = User(
            google_id=me["id"],
            given_name=me["given_name"],
            family_name=me["family_name"],
            picture=me["picture"],
            google_token=resp["access_token"],
            last_login_at=datetime.now(),
            last_login_ip=flask.request.remote_addr,
            login_count=1,
        )
        url = flask.url_for("frontend.edit_profile")
    else:
        user.given_name = me["given_name"]
        user.family_name = me["family_name"]
        user.picture = me["picture"]
        user.google_token = resp["access_token"]
        user.last_login_at = datetime.now()
        user.last_login_ip = flask.request.remote_addr
        user.login_count += 1
        url = flask.url_for("frontend.index")
    db.session.add(user)
    db.session.commit()

    # Log the user in.
    login_user(user, remember=True)
    return flask.redirect(url)


#
# Flask-Login stuff
#


@login_manager.user_loader
def load_user(userid):
    return User.query.filter_by(id=userid).first()


@auth.route("/signup", methods=["GET", "POST"])
def signup():
    if current_user.is_authenticated():
        return flask.redirect(flask.url_for("frontend.index"))

    errors = None
    form = SignupForm()
    if form.validate_on_submit():
        user = User(form.username.data, form.email.data, form.password.data)
        db.session.add(user)
        try:
            db.session.commit()
        except sqlalchemy.exc.IntegrityError:
            errors = ["A user with that name already exists."]
        else:
            send_confirmation(form.email.data, user)
            return "hi"

    return flask.render_template("signup.html", form=form, errors=errors)


@auth.route("/confirm/<username>/<code>")
def confirm(username=None, code=None):
    print("hi")


@auth.route("/login")
def login():
    if current_user.is_authenticated():
        return flask.redirect(flask.url_for("frontend.index"))
    return flask.render_template("login.html")


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return flask.redirect("/")
