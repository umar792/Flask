from flask import Flask
from app.db import init_db
from app.routes import auth

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = "SECRET_KEY",
    app.config['DATABASE'] = 'database.db'

    with app.app_context():
         init_db()
    app.register_blueprint(auth)
    return app