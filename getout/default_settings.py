# -*- coding: utf-8 -*-

# Flask settings.
DEBUG = False
SECRET_KEY = "development key"
PASSWORD_HASH = "bcrypt"
PASSWORD_SALT = "super-awesome-salt"

# Database stuff.
SQLALCHEMY_DATABASE_URI = "postgresql://localhost/getout"

# Mail setup.
MAIL_SERVER = "smtp.mailgun.org"
MAIL_PORT = 465
MAIL_USE_SSL = True
MAIL_USERNAME = None
MAIL_PASSWORD = None
MAIL_ADMIN_ADDRESS = "getout@mg.dfm.io"
