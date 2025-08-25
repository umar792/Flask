from flask import Blueprint , render_template , flash, redirect , url_for , request
from flask_login import login_user , login_required ,current_user , logout_user
from .forms import RegistrationForm
from ..models import User
from app import db


auth = Blueprint("auth", __name__)

@auth.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data
        print(f"Username: {username}, Email: {email}, Password: {password}")
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash("Email already exists.")
            return redirect(url_for("auth.register"))
        is_username = User.query.filter_by(username=username).first()
        if is_username:
            flash("Username already exists.")
            return redirect(url_for("auth.register"))
        new_user = User(
            username=username,
            email=email,
            password=password
        )
        db.session.add(new_user)
        db.session.commit()
        return "Registration Successful"
    else:
        # flash from errors
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"{getattr(form, field).label.text}: {error}")
    return render_template("register.html" ,form=form)


@auth.route("/login" , methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        user = User.query.filter_by(email=email, password=password).first()
        if user:
            flash("Login Successful")
            login_user(user)
            return redirect(url_for("auth.dashboard", name=current_user.username))
        else:
            flash("Invalid Credentials")
            return redirect(url_for("auth.login"))
    return render_template("login.html")

@auth.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html", name=current_user.username)

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.")
    return redirect(url_for("auth.login"))