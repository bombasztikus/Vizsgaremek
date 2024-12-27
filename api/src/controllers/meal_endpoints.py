from flask import jsonify, Blueprint, request
from src.utils import meal_type_to_display_name, meals_to_dto, str_to_enum_value
from ..models import MealType, Meal
from src.exceptions import *
from flask_jwt_extended import jwt_required, current_user

api = Blueprint("meals", __name__, url_prefix="/meals")

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
    calories = request.json.get("calories")
    image_url = request.json.get("image_url")
    description = request.json.get("description")
    meal_type_as_enum = str_to_enum_value(meal_type, MealType)

    created_meal = Meal.create(
        name=name,
        price=price,
        calories=calories,
        image_url=image_url,
        description=description,
        type=meal_type_as_enum
    )

    return jsonify(created_meal.to_dto()), 201