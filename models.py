from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from app import login_manager

db = SQLAlchemy()


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(10), nullable=False)
    last_name = db.Column(db.String(10), nullable=False)
    enrollment = db.Column(db.String(12), nullable=False, unique=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    profile = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"User('{self.first_name}','{self.last_name}', '{self.enrollment}','{self.email}', '{self.profile})"
