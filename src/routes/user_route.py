from flask import Blueprint, request
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, JWTManager, get_jwt, create_refresh_token
from webargs import fields, ValidationError, flaskparser, validate
from webargs.flaskparser import use_args

from src import helper, cache, jwt, cors, db, bcrypt, app
from src.models import User, Account
from .route_use import REGISTER_REQUESTS, LOGIN_REQUESTS

user_route = Blueprint("user_route",__name__, url_prefix="/api")
BANK_NAME= "Umba Microfinance Bank"

@user_route.route("/register", methods=["POST"])
# @use_args(REGISTER_REQUESTS, location="json")
def register_account():
    user_creation_status = False
    try:
        if request.method == "POST":
            data =  request.get_json()
            firstname = data.get("firstname")
            lastname =data.get("lastname")
            email = data.get("email")
            password = data.get("password")
            phone_number = data.get("phone_number")
            
            user_exists = User.query.filter_by(email=email).first() is not None

            if user_exists:
                app.logger.info("Invalid credentials")
                return helper.response_message(message="Invalid credentials", result= "user already exists", status=401)
            else:
                new_user = User(
                    firstname=firstname,
                    lastname=lastname,
                    email=email,
                    password= bcrypt.generate_password_hash(password),
                    phone_number=phone_number,
                    role="guest",
                )
                db.session.add(new_user)
                db.session.commit()
                user_creation_status=True

                if user_creation_status:
                    user = User.query.filter_by(email=email).first()
                    account = Account(
                        account_number=helper.generate_account_number(),
                        bank_name= BANK_NAME,
                        user_id= user.id, 
                        account_balance=0.00
                    )
                    db.session.add(account)
                    db.session.commit()
                return helper.response_message(result={'message':"user account created successfully"})
    except ConnectionError:
        raise ConnectionError
    
@user_route.route("/login", methods=["POST"])
@use_args(LOGIN_REQUESTS, location="json")
def login(args):
    try:
        if request.method == "POST":
            email =  args['email']
            password =  args['password']
            user =  User.query.filter_by(email=email).first()

            if password is None or email is None:
                return helper.response_message(result="Your credentials are empty")
            
            if  user is None:
                return helper.response_message(message="User is not recognised", result={"error": "Unauthorised"}, status="error")
            else:
                token_created= {
                        "access_token": create_access_token(identity=email),
                        "refresh_token": create_refresh_token(identity=email),
                    }
                user.is_login=True
                db.session.commit()
                app.logger.info("Program running correctly")
                return helper.response_message(message="User is logged in", result=token_created)
    except ConnectionError:
        app.logger.info("Connection Error: "+ ConnectionError)
        raise (ConnectionError)
    
@user_route.route("/logout", methods=['DELETE'])
def logout():
    jti = get_jwt()["jti"]
    try:
        return  helper.response_message(msg="Access token revoked", result={'message': "User is logged out!"})
    except ConnectionError:
        raise ConnectionError

@user_route.route("/users")
@jwt_required()
@cache.cached()
# @cors(["*"])
def users():
    # general requesrs 
    try:
        users = User.query.all()
        user_response = [
            {'firstname': user.firstname, "lastname": user.lastname, "email":user.email, "phone": user.phone_number}
            for user in users 
        ]

        return helper.response_message(result=user_response)
    except ConnectionError:
        raise ConnectionError

@user_route.route("/user") 
@jwt_required()
def user_single(user_id):
    try:
        user_id= helper.get_user_id()
        print("user_id", user_id)
        user =  User.query.filter(User.id == user_id).first()
        user_response ={'firstname': user.firstname, "lastname": user.lastname, "email":user.email, "phone": user.phone_number}
        
        return helper.response_message(result= user_response)
    except ConnectionError:
        raise ConnectionError

@user_route.route("/users/<int:user_id>", methods=["PUT"])
@jwt_required()
def update_user(user_id, args):
    try:
        data = request.get_json()
        user_id = helper.get_user_id()
        user_info = User.query.filter(User.id == user_id).first()
        user_info.firstname =  args['firstname']
        user_info.lastname =  args['lastname']
        user_info.phone_number =  args['phone_number']

        db.session.commit()
        return helper.response_message(result= "user is updated!")
    except ConnectionError:
        raise ConnectionError


@user_route.route("/users/activate/<int:user_id>", methods=["PUT"])
@jwt_required()
def activate_user(user_id):
    try:
        if request.method=="PUT":
            user =User.query.filter_by(id=user_id).first()
            user.is_deactivate=True
            db.session.commit()
            return helper.response_message(result="User is active!")
    except ConnectionError:
        raise ConnectionError
    
@user_route.route("/users/deactivate/<int:user_id>", methods=["DELETE"])
@jwt_required()
def deactivate_user(user_id):
    # using the position of a soft delete
    try:
        if  request.method == "DELETE":
            user =  User.query.filter_by(id=user_id).first()
            user.is_deactivate=False
            db.session.commit()
            return helper.response_message(result="user has been deactivated!")
    except ConnectionError:
        raise ConnectionError
    
@user_route.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return helper.response_message(result=current_user)