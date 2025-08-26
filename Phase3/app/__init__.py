from flask import Flask , jsonify
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
import os

load_dotenv()
db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URI")
    db.init_app(app)
    JWTManager(app)
    from .models import User
    migrate.init_app(app , db)

    # register blueprints
    from .Modules.Auth.route import auth
    app.register_blueprint(auth, url_prefix="/auth")

    @app.route("/")
    def home():
        return jsonify({
            'message' : "Flask app is running"
        }), 200


    @app.errorhandler(Exception)
    def handle_exception(e):
        print(f"❌ Error: {e}")
        return jsonify(error=str(e)), 500

    # Example: specific handler for 404
    @app.errorhandler(404)
    def not_found(e):
        return jsonify(error="Route not found"), 404

    return app