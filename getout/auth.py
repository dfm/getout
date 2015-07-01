# -*- coding: utf-8 -*-

from __future__ import division, print_function

__all__ = ["auth"]

import sqlalchemy
from datetime import datetime

import flask
from flask.ext.login import (current_user, login_user, logout_user,
                             login_required)

from .models import db, login_manager, User
from .forms import SignupForm, LoginForm
from .email import send_confirmation

auth = flask.Blueprint("auth", __name__)


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
            errors = [
                "A user with that username or email address already exists."
            ]
        else:
            send_confirmation(form.email.data, user)
            flask.flash("Confirmation email sent.")
            return flask.redirect(flask.url_for("frontend.index"))

    return flask.render_template("signup.html", form=form, errors=errors)


@auth.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated():
        return flask.redirect(flask.url_for("frontend.index"))

    errors = None
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data) \
                or not user.confirmed:
            errors = [
                "Invalid username or password."
            ]
        else:
            login_user(user, remember=form.remember.data)
            flask.flash("Successfully logged in.")

            next_url = flask.request.args.get("next",
                                              flask.url_for("frontend.index"))

            return flask.redirect(next_url)

    return flask.render_template("login.html", form=form, errors=errors)


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    flask.flash("Successfully logged out.")
    return flask.redirect(flask.url_for("frontend.index"))


@auth.route("/confirm/<username>/<code>")
def confirm(username=None, code=None):
    user = User.query.filter_by(username=username).first()
    if user is None or user.confirmation_code != code \
            or datetime.now() > user.confirmation_expiry:
        flask.flash("Invalid username or confirmation code.")
        return flask.redirect(flask.url_for(".signup"))

    # Update the database.
    user.confirmed = True
    db.session.add(user)
    db.session.commit()

    # Redirect to the login page.
    flask.flash("Email address successfully confirmed. "
                "Log in with your credentials.")
    return flask.redirect(flask.url_for(".login"))


@auth.route("/forgot")
def forgot():
    return "Not implemented"
