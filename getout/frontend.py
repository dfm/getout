# -*- coding: utf-8 -*-

from __future__ import division, print_function

__all__ = ["frontend"]

import flask
from flask.ext.login import current_user, login_required

from .models import db
from .forms import SignupForm, ProfileForm

frontend = flask.Blueprint("frontend", __name__, template_folder="templates")


@frontend.route("/")
def index():
    if current_user.is_authenticated():
        return flask.render_template("index.html")
    form = SignupForm()
    return flask.render_template("signup.html", form=form)


@frontend.route("/new", methods=["GET", "POST"])
def new_visit():
    return flask.render_template("new_visit.html")


@frontend.route("/profile", methods=["GET", "POST"])
@login_required
def edit_profile():
    form = ProfileForm(obj=current_user)
    if form.validate_on_submit():
        form.populate_obj(current_user)
        db.session.commit()
        flask.flash("Profile changes saved.")
    return flask.render_template("edit_profile.html", form=form)
