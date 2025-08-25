from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')


    from .auth.route import auth
    app.register_blueprint(auth, url_prefix="/auth")
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"

    @app.route("/")
    def home():
        return "Welcome to the Auth App"

    db.init_app(app)

    with app.app_context():
        db.create_all()

    return app