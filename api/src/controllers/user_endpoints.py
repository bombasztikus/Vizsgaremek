from flask import jsonify, Blueprint
from ..models import User
from src.exceptions import *
from flask_jwt_extended import jwt_required, current_user

api = Blueprint("users", __name__, url_prefix="/users")

@api.get("/<user_id>")
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