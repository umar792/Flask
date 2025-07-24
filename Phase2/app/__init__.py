from flask import Flask , render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager



db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
     app = Flask(__name__ , template_folder="../templates")
     app.config["SECRET_KEY"] = "SECRET_KEY"
     app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shop.db'

     @app.route("/", methods=["GET"])
     def home():
          return render_template("home.html")

     db.init_app(app)
     login_manager.init_app(app)
     login_manager.login_view = "auth.login"

     from app.models import User
     @login_manager.user_loader
     def load_user(user_id):
          return User.query.get(int(user_id))
     

     from app.auth import auth
     app.register_blueprint(auth ,url_prefix="/auth")
     return app