from flask import Response, jsonify, Blueprint, request
from src.utils import meal_type_to_display_name, meals_to_dto, str_to_enum_value, validate_int_request_param
from ..models import MealType, Meal
from src.exceptions import *
from flask_jwt_extended import jwt_required, current_user
from ..security import AuthorizationHandler

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
    AuthorizationHandler.require_employment(
        user=current_user,
        message="Nem rendelkezel a megfelelő jogosultságokkal ételek létrehozásához"
    )

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
def get_individual_meal(meal_id: int):
    meal_id = validate_int_request_param(
        param=meal_id,
        exception=InvalidMealIDException,
    )
        
    meal = Meal.get_by_id_or_exception(meal_id)
    
    return jsonify(meal.to_dto()), 200

@api.delete("/<int:meal_id>")
@jwt_required()
def delete_meal(meal_id: int):
    meal_id = validate_int_request_param(
        param=meal_id,
        exception=InvalidMealIDException,
    )
    
    AuthorizationHandler.require_employment(
        user=current_user,
        message="Nem rendelkezel a megfelelő jogosultságokkal a termék törléséhez"
    )
    
    meal: Meal = Meal.get_by_id_or_exception(meal_id)
    
    meal.delete()

    return Response(status=204)

@api.put("/<int:meal_id>")
@jwt_required()
def update_meal(meal_id: int):
    meal_id = validate_int_request_param(
        param=meal_id,
        exception=InvalidMealIDException,
    )
    
    AuthorizationHandler.require_employment(
        user=current_user,
        message="Nem rendelkezel a megfelelő jogosultságokkal a termék törléséhez"
    )

    meal: Meal = Meal.get_by_id_or_exception(meal_id)
    meal = meal.update_from_dict(request.json)
    
    return jsonify(meal.to_dto()), 200
    