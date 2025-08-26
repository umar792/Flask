from app import db


class User(db.Model):
    id = db.Column(db.Integer , primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(250) , nullable=False)
    role = db.Column(db.String(20), default='user')