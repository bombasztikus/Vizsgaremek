from enum import Enum
from typing import TYPE_CHECKING, List, TypeVar
from src.exceptions import FlashedException, InvalidEnumValueException

if TYPE_CHECKING:
    from src.models import Meal, MealType, User, Order, OrderItem

def meals_to_dto(meals: list["Meal"], type_display_name: str = None, meal_type: str = None) -> dict:
    meal_dtos = []

    for meal in meals:
        if not meal:
            continue
        
        dto = meal.to_dto()
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

# Type variable constrained to Enum
T = TypeVar("T", bound=Enum)

def get_valid_enum_values(en: T) -> List[T]:
    return list(en)

def get_valid_enum_values_str(en: T) -> List[str]:
    return [v.value.upper() for v in get_valid_enum_values(en)]

def is_valid_enum_value(value: str, en: T) -> bool:
    return value.upper() in get_valid_enum_values_str(en)

def str_to_enum_value(value: str, en: T) -> T:
    if not is_valid_enum_value(value, en):
        raise InvalidEnumValueException()

    enum_values = get_valid_enum_values(en)

    for v in enum_values:
        if v.value.upper() == value.strip().upper():
            return v

    raise InvalidEnumValueException()

def meal_type_to_display_name(meal_type: "MealType") -> str:
    names = {
        "MENU": "Menük",
        "FOOD": "Ételek",
        "BEVERAGE": "Italok",
        "DESSERT": "Desszertek"
    }

    return names[meal_type]

def users_to_dto(users: list["User"]) -> dict:
    user_dtos = []

    for user in users:
        if not user:
            continue

        dto = user.to_dto()
        user_dtos.append(dto)

    return {
        "items": user_dtos,
        "is_error": False
    }

def orders_to_dto(orders: list["Order"]) -> dict:
    order_dtos = []

    for order in orders:
        if not order:
            continue

        dto = order.to_dto()
        order_dtos.append(dto)

    return {
        "items": order_dtos,
        "is_error": False
    }

def order_to_dto_with_items(order: "Order", items: list["OrderItem"]) -> dict:
    dto = order.to_dto()

    item_dtos = []

    for item in items:
        if not item:
            continue

        item_dtos.append(item.to_dto())

    dto["items"] = item_dtos

    return dto