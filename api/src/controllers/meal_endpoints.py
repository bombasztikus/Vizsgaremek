from flask import Response, jsonify, Blueprint, request
from src.utils import meal_type_to_display_name, meals_to_dto, str_to_enum_value
from ..models import MealType, Meal
from src.exceptions import *
from flask_jwt_extended import jwt_required, current_user

api = Blueprint("meals", __name__, url_prefix="/meals")

@api.get("")
@jwt_required(optional=True)
def get_all_meals():
    filter_ids = request.args.get("ids", "").split(",")
    limit_per_type = request.args.get("per_category", "")
    
    safe_ids = [int(_id) for _id in filter_ids if _id.isdigit()]
    items = []

    if len(safe_ids) == 0:
        items = Meal.get_all(
            limit_per_type=limit_per_type if limit_per_type.isdigit() else 0
        )
    else:
        items = Meal.get_all_by_ids(safe_ids)
        
    return jsonify(meals_to_dto(items)), 200

@api.get("/<string:meal_type>")
@jwt_required(optional=True)
def get_meal(meal_type: str):
    meal_type_as_enum = str_to_enum_value(meal_type, MealType) 
    items = Meal.get_all_by_type(meal_type_as_enum)
    return jsonify(meals_to_dto(items, meal_type_to_display_name(meal_type_as_enum), meal_type_as_enum)), 200

@api.post("/<string:meal_type>")
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

@api.get("/<int:meal_id>")
@jwt_required(optional=True)
def get_individual_meal(meal_id: str):
    meal = Meal.get_by_id_or_none(id=meal_id)

    if not meal:
        raise MealNotFoundException()
    
    return jsonify(meal.to_dto()), 200

@api.delete("/<int:meal_id>")
@jwt_required()
def delete_meal(meal_id: int):
    if not meal_id:
        raise InvalidMealIDException()
    
    if not current_user or not current_user.is_employee:
        raise UnauthorizedException("Nem rendelkezel a megfelelő jogosultságokkal a termék törléséhez")
    
    try:
        meal = Meal.get_by_id_or_exception(int(meal_id))
        
        meal.delete()
    except ValueError:
        raise InvalidMealIDException()
    
    return Response(status=204)

@api.put("/<int:meal_id>")
@jwt_required()
def update_meal(meal_id: int):
    if not meal_id:
        raise InvalidMealIDException()
    
    if not current_user or not current_user.is_employee:
        raise UnauthorizedException("Nem rendelkezel a megfelelő jogosultságokkal a termék törléséhez")
    
    try:
        meal: Meal = Meal.get_by_id_or_exception(int(meal_id))

        meal = meal.update_from_dict(request.json)
        
        return jsonify(meal.to_dto()), 200
    except ValueError:
        raise InvalidMealIDException()
    