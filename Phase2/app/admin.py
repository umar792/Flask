from flask import Flask , request , flash , render_template , redirect , url_for , Blueprint
from flask_login import current_user
from app.models import User ,Product
import os
from app import db

admin = Blueprint("admin", __name__)

@admin.route("/auth/dashboards")
def index():
    return redirect(url_for("admin.users"))

@admin.route("/users")
def users():
    all_users = User.query.filter_by().all()
    return render_template("dashboard.html",
                           active_tab="users",
                           users=all_users,
                           products=None)


@admin.route("/products")
def products():
    all_products = Product.query.order_by(Product.id.desc()).all()
    return render_template("dashboard.html",
                           active_tab="products",
                           users=None,
                           products=all_products)


@admin.route("/product/create" , methods=["GET","POST"])
def create_product():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        description = request.form.get("description", "").strip()
        price = request.form.get("price", "").strip()
        stock = request.form.get("stock", "").strip()
        image_file = request.files.get("image")

        errors = []
        if not name:
            errors.append("Name is required")
        
        if not description:
            errors.append("Description is required")
        
        try:
            price = float(price)
        except (TypeError, ValueError):
            errors.append("Price must be a number.")

        try:
            if not stock:
                errors.append("Stock must required")
            stock = int(stock)
        except (TypeError, ValueError):
            errors.append("Stock must be an integer.")

        image_path = None
        if image_file or image_file.filename:
            os.makedirs("static/uploads", exist_ok=True)
            save_path = os.path.join("static/uploads", image_file.filename)
            image_file.save(save_path)
            image_path = save_path

        if errors:
            for e in errors:
                flash(e, "error")
                return render_template("dashboard.html",
                                   active_tab="create",
                                   users=None,
                                   products=None)
        product = Product(
            name=name,
            description=description,
            price=price,
            stock=stock,
            image=image_path
        )
        db.session.add(product)
        db.session.commit()
        flash("Product created successfully!", "success")
        return redirect(url_for("admin.products"))
    
    return render_template("dashboard.html",
                           active_tab="create",
                           users=None,
                           products=None)
        


