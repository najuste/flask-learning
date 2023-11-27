import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, render_template
from flask_login import LoginManager, UserMixin
from flask_migrate import Migrate

from db import engine
from config import AppConfig, basedir

app = Flask(__name__)
app.config.from_object(AppConfig)
engine.init_app(app)
migrations_dir = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "migrations"
)
migrate = Migrate(app, engine, directory=migrations_dir)

app.debug = True

# setting the log_in view to use for the users who are not logged in and try to view protected page
login = LoginManager(app)
login.login_view = "login"


@login.user_loader  # helps in storing the uid of Flask user session and this is it's registration
def load_user(id: str):
    return User.query.get(int(id))


class User(UserMixin):
    pass


@login.user_loader
def load_user(user_id):
    # Replace this with the logic to load a user from your database
    user = User()
    user.id = user_id
    return user


from app.routes import main_bp

app.register_blueprint(main_bp)

# careful to import the routes and errors after creating the app,
from app import errors

if __name__ == "__main__":
    app.run(port=5000, host="0.0.0.0")
