from flask import jsonify, Blueprint, request
from src.utils import meal_type_to_display_name, meals_to_dto, str_to_enum_value
from ..models import MealType, Meal
from src.exceptions import *
from flask_jwt_extended import jwt_required, current_user
import werkzeug.exceptions as wkz_exc

api = Blueprint("meals", __name__, url_prefix="/meals")

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

@api.get("/")
@jwt_required(optional=True)
def get_all_meals():
    items = Meal.get_all()
    return jsonify(meals_to_dto(items)), 200

@api.get("/<meal_type>")
@jwt_required(optional=True)
def get_meal(meal_type: str):
    meal_type_as_enum = str_to_enum_value(meal_type, MealType) 
    items = Meal.get_all_by_type(meal_type_as_enum)
    return jsonify(meals_to_dto(items, meal_type_to_display_name(meal_type_as_enum), meal_type_as_enum)), 200

@api.post("/<meal_type>")
@jwt_required()
def post_meal(meal_type: str):
    if not current_user or not current_user.is_employee:
        raise UnauthorizedException("Nem rendelkezel a megfelelő jogosultságokkal ételek létrehozásához")

    name = request.json.get("name")
    price = request.json.get("price")
    currency = request.json.get("currency")
    calories = request.json.get("calories")
    image_url = request.json.get("image_url")
    description = request.json.get("description")
    meal_type_as_enum = str_to_enum_value(meal_type, MealType)

    created_meal = Meal.create(
        name=name,
        price=price,
        currency=currency,
        calories=calories,
        image_url=image_url,
        description=description,
        type=meal_type_as_enum
    )

    return jsonify(created_meal.to_dto()), 201