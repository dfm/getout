# -*- coding: utf-8 -*-

from __future__ import division, print_function

__all__ = ["create_app"]

import flask


def before_first_request():
    pass


def create_app(config_filename=None):
    app = flask.Flask(__name__)
    app.config.from_object("getout.default_settings")
    if config_filename is not None:
        app.config.from_pyfile(config_filename)

    # Set up the extensions.
    from .models import db, login_manager
    db.init_app(app)
    login_manager.init_app(app)

    from .email import mail
    mail.init_app(app)

    # Before request.
    app.before_first_request(before_first_request)

    # Bind the blueprints.
    from .auth import auth
    app.register_blueprint(auth)

    from .frontend import frontend
    app.register_blueprint(frontend)

    return app
