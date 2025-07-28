from flask import Blueprint , render_template , redirect , url_for , flash , request
from app.models import User , CartItem ,Product
from app import db
from app.form import RegistrationForm
from flask_login import login_required ,current_user , login_user , logout_user


auth = Blueprint("auth", __name__)

@auth.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    print("form.validate_on_submit()" , form.validate_on_submit())
    if form.validate_on_submit():
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user:
            flash("Email already exists.", "danger")
            return redirect(url_for("auth.register"))
    
        newUser = User(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data,
            is_admin=False
        )
        db.session.add(newUser)
        db.session.commit()
        flash("Account created successfully, Please login","success")
        return redirect(url_for("auth.login"))

    return render_template("register.html",form=form)


@auth.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email,password=password).first()
        if not user:
            flash("Invalid Credentials")
            return redirect(url_for("auth.login"))
        else:
            login_user(user)
            cartData = CartItem.query.filter_by(user_id=current_user.id).all()
            return redirect(url_for("home",cartData=cartData))
    return render_template("login.html")

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    products = Product.query.filter_by().all()
    return render_template("home.html" , current_user=current_user , products=products)

@auth.route("/dashboard")
@login_required
def dashboard():
    if not current_user.is_authenticated:
        return redirect(url_for("auth.login"))
    return render_template("dashboard.html")








