# -*- coding: utf-8 -*-

from __future__ import division, print_function

__all__ = ["send_email", "send_confirmation"]

import flask
from flask.ext.mail import Mail, Message

from datetime import datetime, timedelta

from .models import db

mail = Mail()


def send_email(subject, body, html, *to_):
    msg = Message(subject,
                  sender=flask.current_app.config["MAIL_ADMIN_ADDRESS"],
                  recipients=list(to_))
    msg.body = body
    msg.html = html
    mail.send(msg)


def send_confirmation(email, user):
    send_email("GetOut email confirmation",
               flask.render_template("emails/confirmation.txt", user=user),
               flask.render_template("emails/confirmation.html", user=user),
               email)
    user.confirmation_expiry = datetime.now() + timedelta(days=10)
    db.session.add(user)
    db.session.commit()
