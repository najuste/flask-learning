# creates engine object that can be shared by both app and api modules

from flask_sqlalchemy import SQLAlchemy

engine = SQLAlchemy()
