# -*- coding: utf-8 -*-

from __future__ import division, print_function

__all__ = ["api"]

import flask
from flask.ext.login import current_user, login_required

from .models import db

api = flask.Blueprint("api", __name__,
                      static_folder="static", template_folder="templates")


@api.route("/")
def index():
    return "blah"


@api.route("/spaces/new")
@login_required
def new_space():
    pass
