# -*- coding: utf-8 -*-

from __future__ import division, print_function

__all__ = ["create_app"]

import flask
from .mail import mail
# from .models import db, security_ext


# def before_first_request():
#     # db.drop_all()
#     db.create_all()


def create_app(config_filename=None):
    app = flask.Flask(__name__)
    app.config.from_object("getout.default_settings")
    if config_filename is not None:
        app.config.from_pyfile(config_filename)

    # # Set up the extensions.
    # db.init_app(app)
    # security_ext.init_app(app)
    # mail.init_app(app)

    # # Before request.
    # app.before_first_request(before_first_request)

    # Bind the blueprints.
    from .auth import auth
    app.register_blueprint(auth)

    return app
