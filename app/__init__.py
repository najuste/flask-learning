import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, render_template
from flask_login import LoginManager, UserMixin
from flask_migrate import Migrate

from db import engine
from conf import AppConfig, basedir

app = Flask(__name__)
app.config.from_object(AppConfig)
engine.init_app(app)
migrate = Migrate(app, engine)

app.debug = True

login = LoginManager(app)
login.login_view = "login"


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
