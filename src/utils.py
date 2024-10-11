from enum import Enum
from typing import TYPE_CHECKING, TypeVar
from src.exceptions import FlashedException, InvalidEnumValueException

if TYPE_CHECKING:
    from src.models import Meal, MealType

def flashed_exception_to_dto(exc: FlashedException) -> dict:
    return {
        "error": exc.flash_message,
        "css_class": exc.css_class,
        "http_code": exc.http_code,
        "is_error": True,
    }

def meals_to_dto(meals: list["Meal"], type_display_name: str = None, meal_type: str = None) -> dict:
    meal_dtos = []

    for meal in meals:
        dto = meal.to_dto()
        dto["display_price"] = currency_to_display_name(meal.currency).format(meal.price)
        meal_dtos.append(dto)

    dto = {
        "items": meal_dtos,
        "is_error": False,
    }

    if type_display_name:
        dto["type_display_name"] = type_display_name
    
    if meal_type:
        dto["type"] = meal_type

    return dto

def get_valid_enum_values(en: Enum) -> list[Enum]:
    return [v.value for v in en]

def get_valid_enum_values_str(en: Enum) -> list[str]:
    return [s for s in get_valid_enum_values()]

def is_valid_enum_value(value: str, en: Enum) -> bool:
    return str(value).upper() in get_valid_enum_values_str(en)

T = TypeVar("T")
def str_to_enum_value(value: str, en: Enum) -> T:
    if not is_valid_enum_value(value, en):
        raise InvalidEnumValueException()
    
    enum_values = get_valid_enum_values(en)

    for v in enum_values:
        if v == str(value).strip().upper():
            return v

    raise InvalidEnumValueException()

def meal_type_to_display_name(meal_type: "MealType") -> str:
    names = {
        "MENU": "Menük",
        "FOOD": "Ételek",
        "BEVERAGE": "Italok"
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