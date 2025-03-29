from flask import jsonify, Blueprint, request
from ..security import AuthenticationHandler
from ..models import User
from src.exceptions import *
from flask_jwt_extended import create_access_token
from datetime import timedelta
from src.validation import validate_dto_or_exception

api = Blueprint("auth", __name__, url_prefix="/auth")
    
@api.post("/login")
def post_obtain_token():
    dto = validate_dto_or_exception(request.json, {
        "email": InvalidEmailException("Az email cím megadása kötelező"),
        "password": InvalidPasswordException("A jelszó megadása kötelező")
    })

    access_token = AuthenticationHandler.flow_JWT(
        email=dto.get("email"),
        password=dto.get("password")
    )
    
    return jsonify(access_token.to_dto()), 201

@api.post("/register")
def post_auth_register():
    dto = validate_dto_or_exception(request.json, {
        "email": InvalidEmailException("Az email cím megadása kötelező"),
        "password": InvalidPasswordException("A jelszó megadása kötelező"),
        "full_name": InvalidFullNameException("A teljes név megadása kötelező")
    })

    email = dto.get("email")
    password = dto.get("password")
    full_name = dto.get("full_name")
    
    created_user = User.create(email, full_name, password, False)

    return jsonify(created_user.to_dto()), 201
