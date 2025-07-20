from flask import Blueprint , request, jsonify
from .models import create_user , login_user


auth = Blueprint("auth", __name__)


@auth.route("/register", methods=["POST"])
def register():
    data  = request.get_json()
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")
    if not username or not email or not password:
        return jsonify({
            'success': False,
            'message': "Username, email, and password are required"
        })
    isCreated = create_user(username,email,password)
    print(isCreated)
    if isCreated["success"] == True:
        return jsonify({
            'success': True,
            'message': "User created successfully",
        }),201
    else:
        return jsonify(isCreated),400
    

@auth.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")
    if not email or not password:
        return jsonify({
            'success': False,
            'message': "Email and password are required"
        }) , 400
    isLoggedIn = login_user(email , password)
    if isLoggedIn["success"] == True:
        return jsonify(isLoggedIn),200
    else:
        return jsonify(isLoggedIn),400