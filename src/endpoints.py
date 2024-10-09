from flask import jsonify, Blueprint

from src.utils import flashed_exception_to_dto, currency_to_display_name, meal_type_to_display_name, meals_to_dto, str_to_meal_type
from .models import User, Meal
from flask_login import login_required, current_user, login_user, logout_user
from src.exceptions import FlashedException, InvalidUserIDException, UserNotFoundException

api = Blueprint('api', __name__, url_prefix='/api')

@api.errorhandler(FlashedException)
def handle_exception(e):
    if isinstance(e, FlashedException):
        return e

    return flashed_exception_to_dto(e), 

@api.get("/meals/<meal_type>")
def meal(meal_type: str):
    try:
        meal_type_as_enum = str_to_meal_type(meal_type)
        if not meal_type_as_enum:
            raise FlashedException("Invalid meal type", "danger")
        
        items = Meal.get_all_by_type(meal_type_as_enum)
        return jsonify(meals_to_dto(items, meal_type_to_display_name(meal_type_as_enum), meal_type_as_enum))
    
    except FlashedException as e:
        return flashed_exception_to_dto(e)
    except Exception as e:
        print(e)
        return flashed_exception_to_dto(FlashedException())
    
@api.get("/users/<user_id>")
def user(user_id: int):
    try:
        if not user_id:
            raise InvalidUserIDException()
        
        try:
            user = User.get_by_id(int(user_id))
            if not user:    
                raise UserNotFoundException()
            
            return jsonify(user.to_dto())
        except ValueError:
            raise InvalidUserIDException()
        
    except FlashedException as e:
        return flashed_exception_to_dto(e)
    except Exception as e:
        print(e)
        return flashed_exception_to_dto(FlashedException())