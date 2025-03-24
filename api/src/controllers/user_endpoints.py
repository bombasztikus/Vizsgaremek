from flask import jsonify, Blueprint
from ..models import User
from src.exceptions import *
from flask_jwt_extended import jwt_required, current_user
from src.utils import users_to_dto

api = Blueprint("users", __name__, url_prefix="/users")

@api.get("/<int:user_id>")
@jwt_required(optional=True)
def get_user(user_id: int):
    if not user_id:
        raise InvalidUserIDException()
    
    try:
        user = User.get_by_id_or_none(int(user_id))
        if not user:    
            raise UserNotFoundException()
        
        if current_user:
            if str(user_id).strip() != current_user.get_id() and not current_user.is_employee:
                raise UnauthorizedException()
        else:
            raise UnauthorizedException()
        
        return jsonify(user.to_dto())
    except ValueError:
        raise InvalidUserIDException()
    
@api.get("")
@jwt_required(optional=False)
def get_users():
    if not current_user or not current_user.is_employee:
        raise UnauthorizedException("Nem rendelkezel a megfelelő jogosultságokkal a felhasználók lekérdezéséhez")
    
    items = User.get_all()
    return jsonify(users_to_dto(items)), 200

@api.get("/me")
@jwt_required()
def get_me():
    try:
        if not current_user:
            raise UnauthorizedException()

        user = User.get_by_id_or_none(current_user.id)
        if not user:
            raise UserNotFoundException()
        
        return jsonify(user.to_dto()), 200
    except ValueError:
        raise InvalidUserIDException()