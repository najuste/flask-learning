from db import engine as db
from datetime import datetime


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), index=True)
    text = db.Column(db.String(150), index=True, nullable=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    created_by_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    assigned_to_id = db.Column(db.Integer, nullable=True)
    done = db.Column(db.Boolean)

    def __repr__(self):
        """method of how the class is going to be printed"""
        return '<Task {}>'.format(self.title)
