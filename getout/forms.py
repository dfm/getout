# -*- coding: utf-8 -*-

from __future__ import division, print_function

__all__ = ["SignupForm"]

from flask_wtf import Form
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Email


class SignupForm(Form):

    username = StringField("username", validators=[
        DataRequired(message="A username is required."),
    ])
    email = StringField("email", validators=[
        DataRequired(message="An email address is required."),
        Email(message="Invalid email address."),
    ])
    password = PasswordField("password", validators=[
        DataRequired(message="A password is required."),
    ])
