from app import db


class User(db.Model):
    # __tablename__ = "if the snake case class name is not desired"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(24), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    tasks = db.relationship('Task', backref='author', lazy='dynamic')

    def __repr__(self):
        """method of how the class is going to be printed"""
        return '<User {}>'.format(self.username)
