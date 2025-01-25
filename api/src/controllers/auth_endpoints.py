from flask import jsonify, Blueprint, request
from ..models import User
from src.exceptions import *
from flask_jwt_extended import create_access_token
from datetime import timedelta

api = Blueprint("auth", __name__, url_prefix="/auth")
    
@api.post("/login")
def post_obtain_token():
    email = request.json.get("email")
    password = request.json.get("password")

    if not email:
        raise InvalidEmailException("Az email cím megadása kötelező")
    elif not password:
        raise InvalidPasswordException("A jelszó megadása kötelező")

    user = User.verify(email, password)

    access_token_expiry = timedelta(days=30)
    access_token = create_access_token(user, expires_delta=access_token_expiry)

    return jsonify({
        "access_token": str(access_token),
        "expiry": int(access_token_expiry.total_seconds())
    }), 200

@api.post("/register")
def post_auth_register():
    email = request.json.get("email")
    password = request.json.get("password")
    full_name = request.json.get("full_name")

    if not email:
        raise InvalidEmailException("Az email cím megadása kötelező")
    elif not password:
        raise InvalidPasswordException("A jelszó megadása kötelező")
    elif not full_name:
        raise InvalidFullNameException("A teljes név megadása kötelező")

    if User.email_taken(email):
        raise EmailUnavailableException()
    
    created_user = User.create(email, full_name, password, False)
    return jsonify(created_user.to_dto()), 201
