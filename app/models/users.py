from datetime import datetime
from hashlib import md5
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login
from flask_login import UserMixin


@login.user_loader # helps in storing the uid of Flask user session and this is it's registration
def load_user(id: str):
    return User.query.get(int(id))


class User(UserMixin, db.Model):
    # __tablename__ = "if the snake case class name is not desired"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(24), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    tasks = db.relationship('Task', backref='author', lazy='dynamic')
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        """method of how the class is going to be printed"""
        return '<User {}>'.format(self.username)

    def set_password(self, password: str):
        self.password_hash = generate_password_hash(password)

    def is_password_correct(self, password: str):
        return check_password_hash(self.password_hash, password)

    def avatar(self):
        email_digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s=50'.format(email_digest)
