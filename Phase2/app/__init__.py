from flask import Flask , render_template ,send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager , current_user 



db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
     app = Flask(__name__ , template_folder="../templates")
     app.config["SECRET_KEY"] = "SECRET_KEY"
     app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shop.db'

   

     db.init_app(app)
     login_manager.init_app(app)
     login_manager.login_view = "auth.login"

     from app.models import User
     @login_manager.user_loader
     def load_user(user_id):
          return User.query.get(int(user_id))
     

     from app.auth import auth
     from app.admin import admin
     app.register_blueprint(auth ,url_prefix="/auth")
     app.register_blueprint(admin)

     @app.route('/uploads/<path:filename>')
     def uploaded_file(filename):
           print(filename)
           return send_from_directory("../static/uploads", filename)
     
     from app.models import Product
     from app.models import CartItem
     @app.route("/", methods=["GET"])
     def home():
          products = Product.query.filter_by().all()
          return render_template("home.html" , current_user=current_user , products=products)
     

     @app.route("/product/detail/<int:id>")
     def detail(id):
          product = Product.query.filter_by(id=id).first()
          return render_template("detail.html", product=product)

     @app.route("/cart/<int:id>")
     def addToCart(id):
          product = Product.query.filter_by(id=id).first()
          item = CartItem.query.filter_by(user_id=current_user.id , product_id=id)
          if item:
               return render_template("detail.html", product=product) 
           
          return render_template("detail.html", product=product) 
     return app