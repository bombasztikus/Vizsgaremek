from typing import Optional
from flask import jsonify, Blueprint, request, Response
from ..security import AuthorizationHandler
from ..models import Meal, Order, OrderItem
from src.exceptions import *
from flask_jwt_extended import jwt_required, current_user
from src.utils import orders_to_dto, order_to_dto_with_items, detailed_order_to_dto, validate_int_request_param
from src.validation import validate_dto_or_exception

api = Blueprint("orders", __name__, url_prefix="/orders")

@api.get("")
@jwt_required()
def get_orders():
    if not current_user:
        raise UnauthorizedException("Nem rendelkezel a megfelelő jogosultságokkal az összes rendelés lekérdezéséhez")
    
    orders = Order.get_all() if current_user.is_employee else Order.get_all_by_user_id(current_user.id)
    return jsonify(orders_to_dto(orders)), 200

@api.get("/<order_id>")
@jwt_required()
def get_order(order_id: int):
    order_id = validate_int_request_param(
        param=order_id,
        exception=InvalidOrderIDException()
    )

    order: Order = Order.get_by_id_or_exception(order_id)

    AuthorizationHandler.require_employment_or_ownership(
        user=current_user,
        owner_user_id=order.user_id
    )    
    
    order_items = order.get_items()

    return jsonify(order_to_dto_with_items(
        order=order,
        items=order_items
    )), 200

@api.post("")
@jwt_required()
def post_order():
    address = request.json.get("address", None)
    items = request.json.get("items", [])

    if len(items) == 0:
        raise InvalidPayloadException("A rendeléshez legalább 1 tétel megadása szükséges")
    elif not address:
        raise InvalidAddressException()

    created_order: Order = Order.create(
        user_id=current_user.id,
        address=address,
    )

    created_items = []
    for item in items:
        meal_id = item.get("id")
        quantity = item.get("quantity")

        if not meal_id:
            raise InvalidMealIDException()
        elif not quantity:
            raise InvalidQuantityException()
        
        created_items.append(created_order.add_item(
            meal_id=meal_id,
            quantity=quantity
        ))

    return jsonify(order_to_dto_with_items(
        order=created_order,
        items=created_items
    )), 201

@api.put("/<order_id>")
@jwt_required()
def put_order(order_id: int):
    order_id = validate_int_request_param(
        param=order_id,
        exception=InvalidOrderIDException()
    )
    
    AuthorizationHandler.require_employment(
        user=current_user,
        message="Nem rendelkezel a megfelelő jogosultságokkal a rendelés utólagos módosításához"
    )
    
    order: Order = Order.get_by_id_or_exception(order_id)

    address = request.json.get("address", None)

    if address:
        order = order.set_address(address)
    is_completed = request.json.get("is_completed", None)

    if isinstance(is_completed, bool):
        order = order.set_is_completed(is_completed)
    
    return jsonify(order.to_dto()), 200

@api.delete("/<order_id>")
@jwt_required()
def delete_order(order_id: int):
    order_id = validate_int_request_param(
        param=order_id,
        exception=InvalidOrderIDException()
    )
    
    AuthorizationHandler.require_employment(
        user=current_user,
        message="Nem rendelkezel a megfelelő jogosultságokkal a rendelés törléséhez"
    )
    
    order = Order.get_by_id_or_exception(order_id)
    
    OrderItem.delete_all(order)
    order.delete()
    
    return Response(status=204)

@api.put("/<order_id>/items/<item_id>")
@jwt_required()
def update_order_item(order_id: int, item_id: int):
    order_id = validate_int_request_param(
        param=order_id,
        exception=InvalidOrderIDException()
    )

    item_id = validate_int_request_param(
        param=item_id,
        exception=InvalidOrderItemIDException()
    )

    AuthorizationHandler.require_employment(
        user=current_user,
        message="Nem rendelkezel a megfelelő jogosultságokkal a rendelés elemeinek frissítéséhez"
    )

    item = OrderItem.get_by_id_or_exception(
        order_id=order_id,
        meal_id=item_id
    )

    dto = validate_dto_or_exception(dto=request.json, fields={
        "quantity": InvalidQuantityException()
    })

    quantity = dto.get("quantity")

    item.set_quantity(quantity)
    
    return jsonify(item.to_dto()), 200

@api.post("/<order_id>/items")
@jwt_required()
def add_order_item(order_id: int):
    order_id = validate_int_request_param(
        param=order_id,
        exception=InvalidOrderIDException()
    )

    AuthorizationHandler.require_employment(
        user=current_user,
        message="Nem rendelkezel a megfelelő jogosultságokkal a rendelés elemeinek hozzáadásához"
    )

    order: Order = Order.get_by_id_or_exception(order_id)

    dto = validate_dto_or_exception(dto=request.json, fields={
        "id": InvalidMealIDException(),
        "quantity": InvalidQuantityException()
    })

    quantity = dto.get("quantity")
    meal_id = dto.get("id")

    new_item = order.add_item(
        meal_id=meal_id,
        quantity=quantity
    )

    return jsonify(new_item.to_dto()), 201

@api.delete("/<order_id>/items/<item_id>")
@jwt_required()
def delete_order_item(order_id: int, item_id: int):
    order_id = validate_int_request_param(
        param=order_id,
        exception=InvalidOrderIDException()
    )

    item_id = validate_int_request_param(
        param=item_id,
        exception=InvalidOrderItemIDException()
    )
    
    AuthorizationHandler.require_employment(
        user=current_user,
        message="Nem rendelkezel a megfelelő jogosultságokkal a rendelés elemeinek törléséhez"
    )
    
    order: Order = Order.get_by_id_or_exception(order_id)

    if order.get_item_count() == 1:
        raise OrderItemUndeletableException("A rendelés utolsó tétele nem törölhető mert a rendelésnek legalább 1 db. tétele kell legyen")

    item = OrderItem.get_by_id_or_exception(
        order_id=order_id,
        meal_id=item_id
    )
        
    item.delete()
    
    return Response(status=204)

@api.get("/<order_id>/items")
@jwt_required()
def get_order_items(order_id: int):
    order_id = validate_int_request_param(
        param=order_id,
        exception=InvalidOrderIDException()
    )
    
    AuthorizationHandler.require_employment(
        user=current_user,
        message="Nem rendelkezel a megfelelő jogosultságokkal a rendelés elemeinek frissítéséhez"
    )
    
    order: Order = Order.get_by_id_or_exception(order_id)

    items = order.get_detailed_items()
    
    return jsonify(detailed_order_to_dto(
        the_order=order,
        order_items=items
    )), 200