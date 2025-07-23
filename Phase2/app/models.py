from app import db
from flask_login import UserMixin
from datetime import datetime


class User(UserMixin , db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer , primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(256),nullable=False)
    is_admin = db.Column(db.Boolean , default=False)

    orders = db.relationship("Order", backref="user", lazy=True)
    cart_items = db.relationship("CartItem", backref="user", lazy=True)
    


class Product(db.Model):
    __tablename__ = "products"

    id  = db.Column(db.Integer , primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text , nullable=False)
    price = db.Column(db.Float , nullable=False)
    stock = db.Column(db.Integer , default=0)
    image = db.Column(db.String(256))

class CartItem(db.Model):
    __tablename__ = "cart_items"

    id = db.Column(db.Integer , primary_key=True)
    quantity = db.Column(db.Integer , default=1)
    user_id = db.Column(db.Integer , db.ForeignKey('users.id')) # one way relation so thats why we don't use the cartItem id in users
    product_id  = db.Column(db.Integer , db.ForeignKey('products.id'))

    product = db.relationship("Product") # one way relation so we add this 


class Order(db.Model):
    __tablename__ = "orders"

    id = db.Column(db.Integer , primary_key=True)
    created_at = db.Column(db.DateTime , default=datetime.utcnow)
    user_id = db.Column(db.Integer , db.ForeignKey('users.id'))
    status = db.Column(db.String(150), default="Pending")

    items = db.relationship('OrderItem', backref="order", lazy=True)
    payment = db.relationship("Payment", backref='order', lazy=True,uselist=False)
    

class OrderItem(db.Model):
    __tablename__ = "order_items"

    id = db.Column(db.Integer , primary_key=True)
    order_id = db.Column(db.Integer , db.ForeignKey('orders.id'))
    product_id = db.Column(db.Integer , db.ForeignKey('products.id'))
    quantity = db.Column(db.Integer , default=1)

    product = db.relationship('Product')



class Payment(db.Model):
    __tablename__ = "payments"


    id = db.Column(db.Integer , primary_key=True)
    payment_intent_id = db.Column(db.String(100))
    status = db.Column(db.String(50))
    amount= db.Column(db.Float)
    created_at  = db.Column(db.DateTime , default=datetime.utcnow)
    order_id = db.Column(db.Integer , db.ForeignKey('orders.id'), nullable=False)