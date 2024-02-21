from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_session import Session
from flask_migrate import Migrate
from flask_mail import Mail

app = Flask(__name__)

bcrypt = Bcrypt(app)

app.config.from_object("config")
Session(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# mail send karva mate
mail = Mail(app)

from app import routes, models
