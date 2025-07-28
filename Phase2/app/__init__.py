from flask import Flask , render_template ,send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager , current_user  ,login_required
from sqlalchemy.orm import  selectinload




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
     from app.models import CartItem , Order , OrderItem , Payment
     @app.route("/", methods=["GET"])
     def home():
          products = Product.query.filter_by().all()
          CartItems = CartItem.query.filter_by(user_id=current_user.id).all()
          return render_template("home.html" , current_user=current_user , products=products,cartData=CartItems)
     
     @app.route("/cart", methods=["GET"])
     def cart():
          CartItems = CartItem.query.options(selectinload(CartItem.product)).filter_by(user_id=current_user.id).all()
          tax=4
          Shipping=2
          subTotal=0
          for cart in CartItems:
               subTotal = subTotal + cart.product.price
          total=tax + Shipping + subTotal
          return render_template("cart.html" , current_user=current_user ,cartData=CartItems ,tax=tax ,Shipping=Shipping,subTotal=subTotal, total=total)
     
     @app.route("/cart/delete/<int:id>")
     def deleteItem(id):
          deleteCartItem = CartItem.query.get(id)
          db.session.delete(deleteCartItem)
          db.session.commit()
          CartItems = CartItem.query.options(selectinload(CartItem.product)).filter_by(user_id=current_user.id).all()
          tax=4
          Shipping=2
          subTotal=0
          for cart in CartItems:
               subTotal = subTotal + cart.product.price
          total=tax + Shipping + subTotal
          return render_template("cart.html" , current_user=current_user ,cartData=CartItems ,tax=tax ,Shipping=Shipping,subTotal=subTotal, total=total)
     
     @app.route("/create/order")
     def createOrder():
          CartItems = CartItem.query.filter_by(user_id=current_user.id).all()
          tax=4
          Shipping=2
          subTotal=0
          for cart in CartItems:
               subTotal = subTotal + cart.product.price
          total=tax + Shipping + subTotal

          # create orders 
          newOrder = Order(
               user_id = current_user.id,
               status = "Paid"
          )

          db.session.add(newOrder)
          db.session.flush()

          # create orderItems
          for cart in CartItems:
               newCartItems = OrderItem(
                    order_id = newOrder.id,
                    product_id = cart.product_id,
                    quantity = 1
               )
               db.session.add(newCartItems)

          # create payment
          newPayment = Payment(
               payment_intent_id = "abebfjefbweofb",
               status = "Paid",
               amount=total,
               order_id=newOrder.id
          )
          db.session.add(newPayment)

          # delete all cart items of the user
          for cart in CartItems:
               db.session.delete(cart)
          
          db.session.commit()

          products = Product.query.filter_by().all()
          return render_template("home.html" , current_user=current_user , products=products,)
     
     @app.route("/orders")
     @login_required
     def orders():
          orders = (
               Order.query
               .options(
                    selectinload(Order.items).selectinload(OrderItem.product)
               )
               .filter_by(user_id=current_user.id)
               .all()
          )

          for order in orders:
               order.total_amount = sum(
                    item.product.price * item.quantity for item in order.items
               )

          return render_template("order.html", current_user=current_user, orders=orders)



     

     @app.route("/product/detail/<int:id>")
     def detail(id):
          product = Product.query.filter_by(id=id).first()
          CartItems = CartItem.query.filter_by(user_id=current_user.id).all()
          return render_template("detail.html", product=product,cartData=CartItems)

     @app.route("/cart/<int:id>")
     def addToCart(id):
          product = Product.query.filter_by(id=id).first()
          item = CartItem.query.filter_by(user_id=current_user.id , product_id=id).first()
          if item:
               CartItems = CartItem.query.filter_by(user_id=current_user.id).all()
               return render_template("detail.html", product=product , cartData=CartItems) 
          else:
               newCartItem = CartItem(
                    user_id =current_user.id,
                    product_id =id
               )
               db.session.add(newCartItem)
               db.session.commit()
               item = CartItem.query.filter_by(user_id=current_user.id).all()
               return render_template("detail.html", product=product , cartData=item) 
     return app