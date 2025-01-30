from typing import Optional
from flask import jsonify, Blueprint, request
from ..models import Order
from src.exceptions import *
from flask_jwt_extended import jwt_required, current_user
from src.utils import orders_to_dto, order_to_dto_with_items

api = Blueprint("orders", __name__, url_prefix="/orders")

@api.get("/")
@jwt_required()
def get_orders():
    if not current_user:
        raise UnauthorizedException("Nem rendelkezel a megfelelő jogosultságokkal az összes rendelés lekérdezéséhez")
    
    orders = Order.get_all() if current_user.is_employee else Order.get_all_by_user_id(current_user.id)
    return jsonify(orders_to_dto(orders)), 200

@api.get("/<order_id>")
@jwt_required()
def get_order(order_id: int):
    if not order_id:
        raise InvalidOrderIDException()
    
    try:
        order = Order.get_by_id_or_none(int(order_id))
        if not order:    
            raise OrderNotFoundException()
        
        if current_user:
            if (order.user_id != current_user.id) or (not current_user.is_employee):
                raise UnauthorizedException()
            
            order_items = order.get_items()
            return jsonify(order_to_dto_with_items(
                order=order,
                items=order_items
            )), 200
        else:
            raise UnauthorizedException()
    except ValueError:
        raise InvalidOrderIDException()

@api.post("/")
@jwt_required()
def post_order():
    if not current_user:
        raise UnauthorizedException("A rendelés létrehozásához bejelentkezés szükséges")
    
    # {
    #     "address": "string",
    #     "items": [
    #         {
    #             "id": 0,
    #             "quantity": 0
    #         }
    #     ]
    # }

    address = request.json.get("address", None)
    items = request.json.get("items", [])

    if len(items) == 0:
        raise InvalidPayloadException("A rendelésnek tartalmaznia kell elemeket")

    created_order: Order = Order.create(
        user_id=current_user.id,
        address=address,
    )

    created_items = []
    for item in items:
        created_items.append(created_order.add_item(
            meal_id=item.get("id"),
            quantity=item.get("quantity")
        ))

    return jsonify(order_to_dto_with_items(
        order=created_order,
        items=created_items
    )), 201

@api.put("/<order_id>")
@jwt_required()
def put_order(order_id: int):
    return jsonify({}), 200

@api.delete("/<order_id>")
@jwt_required()
def delete_order(order_id: int):
    return jsonify({}), 200