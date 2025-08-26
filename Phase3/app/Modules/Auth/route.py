from flask import Blueprint , request, jsonify
from app import db
from app.models import User
from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token , jwt_required, get_jwt_identity
from datetime import timedelta

auth = Blueprint('auth', __name__)
bcrypt = Bcrypt()


#  registration 
@auth.route("/register", methods=["POST"])
def register():
    try:
        data = request.get_json()
        username = data.get("username")
        email = data.get("email")
        password = data.get("password")
        if not username or not email or not password:
            return jsonify({
                'success' : False,
                'error' : "Username, email, and password are required",
            }) , 400

        # check is userName already exists
        isUserName = User.query.filter_by(username=username).first()
        if isUserName:
            return jsonify({
                'success' : False,
                "error" : "Username already exists",
            }) , 400
        
        # check is email already exists
        isEmail = User.query.filter_by(email=email).first()
        if isEmail:
            return jsonify({
                'success': False,
                'error' : "Email already exists",
            }) , 400
        
        # hash the password
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        newUser = User(
            username=username,
            email=email,
            password=hashed_password
        )
        db.session.add(newUser)
        db.session.commit()
        return jsonify({"message": "User registered successfully" , "user": {
                        "id": newUser.id,
                        "username": newUser.username,
                        "email": newUser.email,
                        "role" : "user"
                     }}), 201
    except Exception as e:
        return jsonify({
            'success' : False,
            'error' : str(e)
        })


@auth.route("/login", methods=["POST"])
def login():
    try:
        data = request.get_json()
        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            return jsonify({
                'success' : False,
                'error' : "Email and password are required"
            }), 400
        
        # check email exists
        isEmail = User.query.filter_by(email=email).first()
        if not isEmail:
            return jsonify({
                'success' :False,
                "error" : "Invalid email or password"
            }) , 400
        
        # check password
        isMatch = bcrypt.check_password_hash(isEmail.password, password)
        if not isMatch:
            return jsonify({
                'success' : False,
                'error' : "Invalid email or password"
            })
        

        # create JWT token
        access_token = create_access_token(identity=str(isEmail.id), expires_delta=timedelta(hours=1))
        return jsonify({
            'success' : True,
            "message" : "Login successful",
            'user' : {
                "id": isEmail.id,
                "username": isEmail.username,
                "email": isEmail.email,
                "role" : isEmail.role
            },
            'token' : access_token,
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error' : str(e)
        })
    
@auth.route("/profile")
@jwt_required()
def profile():
    user_id  = get_jwt_identity()
    if not user_id:
        return jsonify({
            'success' : False,
            'error' : "Invalid token or user not found"
        }) , 401
    user = User.query.filter_by(id=int(user_id)).first()
    if not user:
        return jsonify({
            'success' : False,
            'error' : "User not found"
        }) , 404
    return jsonify({
        'success' : True,
        'user' :  {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "role" : user.role
        }
    })
