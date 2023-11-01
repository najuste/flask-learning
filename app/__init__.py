from flask import Flask
from flask_login import LoginManager

from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.debug = True
app.config.from_object(Config)

# setting the log_in view to use for the users who are not logged in and try to view protected page
login = LoginManager(app)
login.login_view = 'login'

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import routes, models
