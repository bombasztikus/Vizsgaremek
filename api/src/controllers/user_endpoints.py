from flask import jsonify, Blueprint
from ..models import User
from src.exceptions import *
from flask_jwt_extended import jwt_required, current_user
import werkzeug.exceptions as wkz_exc

api = Blueprint("users", __name__, url_prefix="/users")

@api.app_errorhandler(FlashedException)
def handle_exception(e):
    return jsonify(e.to_dto()), int(e.http_code)

@api.app_errorhandler(wkz_exc.NotFound)
def not_found(e):
    _ = NotFoundException()
    return jsonify(_.to_dto()), int(_.http_code)

@api.app_errorhandler(Exception)
def wildcard_exception(e):
    if isinstance(e, FlashedException):
        return e
    elif isinstance(e, wkz_exc.HTTPException):
        r = e.get_response()
        _ = FlashedException(flash_message=e.name, http_code=r.status_code)
        return jsonify(_.to_dto()), int(_.http_code)
    
    print(e)
    _ = FlashedException()
    return jsonify(_.to_dto()), int(_.http_code)

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