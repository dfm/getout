# -*- coding: utf-8 -*-

from __future__ import division, print_function

__all__ = ["SignupForm", "LoginForm", "ProfileForm"]

from flask_wtf import Form
from wtforms.validators import DataRequired, Email
from wtforms import StringField, PasswordField, BooleanField


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


class LoginForm(Form):

    username = StringField("username", validators=[
        DataRequired(message="A username is required."),
    ])
    password = PasswordField("password", validators=[
        DataRequired(message="A password is required."),
    ])
    remember = BooleanField("remember")


class ProfileForm(Form):

    given_name = StringField("given_name")
    family_name = StringField("family_name")
    location = StringField("location")
    bio = StringField("bio")
