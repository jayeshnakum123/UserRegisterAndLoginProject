import os

BASEDIR = os.path.abspath(os.path.dirname(__file__))
print(BASEDIR)

# SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:jayesh12345@localhost/app"

SQLALCHEMY_DATABASE_URI = "mysql://root:jayesh12345@localhost/app"

SQLALCHEMY_TRACK_MODIFICATIONS = False

SECRET_KEY = "this-really-needs-to-be-changed"
