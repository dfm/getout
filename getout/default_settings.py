# -*- coding: utf-8 -*-

# Flask settings.
DEBUG = False
SECRET_KEY = "development key"

# Database stuff.
SQLALCHEMY_DATABASE_URI = "postgresql://localhost/getout"

# Mail setup.
MAIL_SERVER = "smtp.mailgun.org"
MAIL_PORT = 465
MAIL_USE_SSL = True
MAIL_USERNAME = None
MAIL_PASSWORD = None

# Security stuff.
SECURITY_PASSWORD_HASH = "bcrypt"
SECURITY_PASSWORD_SALT = "super-awesome-salt"
SECURITY_CONFIRMABLE = True
SECURITY_REGISTERABLE = True
SECURITY_RECOVERABLE = True
SECURITY_TRACKABLE = True
SECURITY_CHANGEABLE = True
