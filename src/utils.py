from src.exceptions import FlashedException
from src.models import Meal, MealType


def flashed_exception_to_dto(exc: FlashedException) -> dict:
    return {
        "error": exc.flash_message,
        "css_class": exc.css_class
    }

def meals_to_dto(meals: list[Meal], type_display_name: str = None, meal_type: str = None) -> dict:
    meal_dtos = []

    for meal in meals:
        dto = meal.to_dto()
        dto["display_price"] = currency_to_display_name(meal.currency).format(meal.price)
        meal_dtos.append(dto)

    dto = {
        "items": meal_dtos
    }

    if type_display_name:
        dto["type_display_name"] = type_display_name
    
    if meal_type:
        dto["type"] = meal_type

    return dto

def get_valid_meal_types() -> list[str]:
    return [e.value.upper() for e in MealType]

def is_valid_meal_type(value: str) -> bool:
    return str(value).upper() in get_valid_meal_types()

def str_to_meal_type(value: str) -> MealType | None:
    match str(value).upper().strip():
        case MealType.MENU:
            return MealType.MENU
        case MealType.FOOD:
            return MealType.FOOD
        case MealType.BEVERAGE:
            return MealType.BEVERAGE
        case _:
            return None
        
def meal_type_to_display_name(meal_type: MealType) -> str:
    names = {
        MealType.MENU: "Menük",
        MealType.FOOD: "Ételek",
        MealType.BEVERAGE: "Italok"
    }

    return names[meal_type]

def currency_to_display_name(value: str) -> str:
    value = str(value).strip().upper()

    match value:
        case "HUF":
            return "{} Ft"
        case "EUR":
            return "{}€"
        case "USD":
            return "${}"
        case "JPY":
            return "¥{}"
        case _:
            return "{} " + value