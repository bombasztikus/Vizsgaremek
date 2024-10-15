from flask import jsonify, Blueprint, request
from src.utils import meal_type_to_display_name, meals_to_dto, str_to_enum_value
from .models import MealType, User, Meal
from src.exceptions import *
from flask_jwt_extended import jwt_required, current_user, create_access_token, create_refresh_token
import werkzeug.exceptions as wkz_exc
from datetime import timedelta

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
    if isinstance(e, FlashedException):
        return e
    elif isinstance(e, wkz_exc.HTTPException):
        r = e.get_response()
        _ = FlashedException(flash_message=e.name, http_code=r.status_code)
        return jsonify(_.to_dto()), int(_.http_code)
    
    print(e)
    _ = FlashedException()
    return jsonify(_.to_dto()), int(_.http_code)

@api.get("/meals/<meal_type>")
@jwt_required(optional=True)
def get_meal(meal_type: str):
    meal_type_as_enum = str_to_enum_value(meal_type, MealType) 
    items = Meal.get_all_by_type(meal_type_as_enum)
    return jsonify(meals_to_dto(items, meal_type_to_display_name(meal_type_as_enum), meal_type_as_enum)), 200
    
@api.get("/users/<user_id>")
@jwt_required(optional=True)
def get_user(user_id: int):
    if not user_id:
        raise InvalidUserIDException()
    
    try:
        user = User.get_by_id_or_none(int(user_id))
        if not user:    
            raise UserNotFoundException()
        
        if not current_user or str(user_id).strip() != current_user.get_id():
            raise UnauthorizedException()
        
        return jsonify(user.to_dto())
    except ValueError:
        raise InvalidUserIDException()
    
@api.post("/auth/login")
def post_obtain_token():
    email = request.json.get("email")
    password = request.json.get("password")

    user = User.verify(email, password)

    access_token_expiry = timedelta(days=30)
    access_token = create_access_token(user, expires_delta=access_token_expiry)

    return jsonify({
        "access_token": str(access_token),
        "expiry": int(access_token_expiry.total_seconds())
    }), 200

@api.post("/auth/register")
def post_auth_register():
    email = request.json.get("email")
    password = request.json.get("password")
    full_name = request.json.get("full_name")

    if User.email_taken(email):
        return UserCreationException(flash_message="Az email cím már foglalt", http_code=409)
    
    created_user = User.create(email, full_name, password, False)
    return jsonify(created_user.to_dto()), 201