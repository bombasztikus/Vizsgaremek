from flask import jsonify, Blueprint, request, Response

from ..security import AuthorizationHandler
from ..models import User
from src.exceptions import *
from flask_jwt_extended import jwt_required, current_user
from src.utils import users_to_dto, validate_int_request_param

api = Blueprint("users", __name__, url_prefix="/users")

@api.get("/<int:user_id>")
@jwt_required(optional=True)
def get_user(user_id: int):
    user_id = validate_int_request_param(
        param=user_id,
        exception=InvalidUserIDException()
    )
    
    user: User = User.get_by_id_or_exception(user_id)

    AuthorizationHandler.require_employment_or_ownership(
        user=current_user,
        owner_user_id=user_id
    )
        
    return jsonify(user.to_dto()), 200
    
@api.put("/<int:user_id>")
@jwt_required()
def update_user(user_id: int):
    user_id = validate_int_request_param(
        param=user_id,
        exception=InvalidUserIDException()
    )
    
    AuthorizationHandler.require_employment(
        user=current_user,
        message="Nem rendelkezel a megfelelő jogosultságokkal a felhasználói adatok frissítéséhez"
    )
    
    user: User = User.get_by_id_or_exception(user_id)
    
    user = user.update_from_dict(request.json)

    return jsonify(user.to_dto()), 200
    
@api.get("")
@jwt_required(optional=False)
def get_users():
    AuthorizationHandler.require_employment(
        user=current_user,
        message="Nem rendelkezel a megfelelő jogosultságokkal a felhasználók lekérdezéséhez"
    )
    
    items = User.get_all()

    return jsonify(users_to_dto(items)), 200

@api.get("/me")
@jwt_required()
def get_me():
    user = User.get_by_id_or_exception(current_user.id)

    return jsonify(user.to_dto()), 200
    
@api.delete("/<int:user_id>")
@jwt_required()
def delete_user(user_id: int):
    user_id = validate_int_request_param(
        param=user_id,
        exception=InvalidUserIDException()
    )

    AuthorizationHandler.require_employment(
        user=current_user,
        message="Nem rendelkezel a megfelelő jogosultságokkal a felhasználók törléséhez"
    )
    
    if user_id == current_user.id:
        raise UnauthorizedException("Nem törölheted a saját fiókodat")
        
    user: User = User.get_by_id_or_exception(user_id)
    if user.is_employee:
        raise UnauthorizedException("Az alkalmazotti típusú fiókok nem törölhetőek")

    user.delete()
    
    return Response(status=204)