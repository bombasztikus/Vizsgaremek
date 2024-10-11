from flask import jsonify, Blueprint
from src.utils import meal_type_to_display_name, meals_to_dto, str_to_enum_value
from .models import MealType, User, Meal
from src.exceptions import *
from flask_jwt_extended import jwt_required, current_user
import werkzeug.exceptions as wkz_exc

api = Blueprint('api', __name__, url_prefix='/api')

@api.app_errorhandler(FlashedException)
def handle_exception(e):
    return jsonify(e.to_dto()), int(e.http_code)

@api.app_errorhandler(wkz_exc.NotFound)
def not_found(e):
    _ = NotFoundException()
    return jsonify(_.to_dto()), int(_.http_code)

@api.app_errorhandler(Exception)
def wildcard_exception(e):
    if isinstance(e, FlashedException) or isinstance(e, wkz_exc.HTTPException):
        return e
    
    print(e)
    _ = FlashedException()
    return jsonify(_.to_dto()), int(_.http_code)

@api.get("/meals/<meal_type>")
def get_meal(meal_type: str):
    meal_type_as_enum = str_to_enum_value(meal_type, MealType) 
    items = Meal.get_all_by_type(meal_type_as_enum)
    return jsonify(meals_to_dto(items, meal_type_to_display_name(meal_type_as_enum), meal_type_as_enum)), 200
    
@api.get("/users/<user_id>")
@jwt_required()
def get_user(user_id: int):
    if not user_id:
        raise InvalidUserIDException()
    
    try:
        user = User.get_by_id_or_none(int(user_id))
        if not user:    
            raise UserNotFoundException()
        
        if str(user_id).strip() != current_user.get_id():
            raise UnauthorizedException()
        
        return jsonify(user.to_dto())
    except ValueError:
        raise InvalidUserIDException()