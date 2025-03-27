from datetime import datetime, timezone
from typing import Optional, Self
import enum
from src.exceptions import *
from sqlalchemy import exc, select, text
from sqlalchemy.orm import aliased
from sqlalchemy.sql import func, over
from flask import request
from src.utils import is_valid_enum_value, str_to_enum_value
from src.validation import *
from . import db
from argon2 import PasswordHasher
from argon2 import exceptions as ph_exc
from sqlalchemy import Column, Integer, String, Boolean, Enum as sqla_Enum, DateTime, ForeignKey
import traceback

ph = PasswordHasher()

class User(db.Model):
    __tablename__ = "Users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(255), unique=True, nullable=False)
    full_name = Column(String(255), unique=False, nullable=False)
    is_employee = Column(Boolean, unique=False, nullable=False, default=False)
    password = Column(String(255), unique=False, nullable=False)

    def __repr__(self):
        return f"<User {self.id} ({self.email})>"
    
    @staticmethod  
    def get_by_id_or_none(id: int) -> Self | None:
        try:
            return db.session.query(User).filter_by(id=id).first()
        except:
            print(traceback.format_exc())
            return None
    
    @staticmethod
    def get_all() -> list[Self]:
        users = db.session.query(User).all()
        return users

    @staticmethod
    def create(email: str, full_name: str, password: str, is_employee: bool = False) -> Self:
        try:
            email = validate_email(email)
            
            email_exists = db.session.query(User.email).filter_by(email=email).scalar()
            if email_exists:
                raise UserCreationException("Az email cím már használatban van")

            full_name = validate_full_name(full_name)

            password = validate_password(password)

            new_user = User(
                email = email,
                full_name = full_name,
                password = ph.hash(password),
                is_employee = is_employee,
            )

            db.session.add(new_user)
            db.session.commit()
            db.session.refresh(new_user)

            return new_user
        except exc.IntegrityError:
            print(traceback.format_exc())
            db.session.rollback()
            raise UserCreationException()
    
    @staticmethod
    def verify(email: str, password: str) -> Self:
        if not email:
            raise InvalidEmailException("Az email cím megadása kötelező")
        elif not password:
            raise InvalidPasswordException("A jelszó megadása kötelező")

        try:
            email = validate_email(email)
            user = db.session.query(User).filter_by(email=email).first()

            if not user:
                raise InvalidCredentialsException()
            
            password_valid = ph.verify(user.password, password)
            if not password_valid:
                raise InvalidCredentialsException()

            return user
        except ph_exc.VerificationError:
            print(traceback.format_exc())
            raise InvalidCredentialsException()

    def get_id(self):
        return str(self.id)
    
    def to_dto(self) -> dict:
        return {
            "id": int(self.id),
            "email": str(self.email),
            "full_name": str(self.full_name),
            "is_employee": bool(self.is_employee),
            "is_error": False,
        }

    @staticmethod
    def email_taken(email: str) -> bool:
        user = db.session.query(User.email).filter_by(email=email).first()
        return True if user else False
    
    @staticmethod
    def get_by_id_or_exception(id: int) -> Self:
        try:
            result = db.session.query(User).filter_by(id=id).first()
            if result is None:
                raise UserNotFoundException()
            
            return result
        except:
            print(traceback.format_exc())
            raise UserNotFoundException()
        
    def update_from_dict(self, values: dict) -> Self:
        commit_changes = False

        if "full_name" in values:
            self.full_name = validate_full_name(values.get("full_name", None))
            commit_changes = True
        
        if "email" in values:
            self.email = validate_email(values.get("email", None))
            commit_changes = True

        if "is_employee" in values and isinstance(values.get("is_employee", None), bool) and values.get("is_employee") != self.is_employee:
            self.is_employee = values.get("is_employee")
            commit_changes = True

        if commit_changes:
            db.session.add(self)
            db.session.commit()
        
        db.session.refresh(self)
        
        return self
    
    def delete(self) -> None:
        db.session.delete(self)
        db.session.commit()

class MealType(str, enum.Enum):
    BEVERAGE = "BEVERAGE"
    FOOD = "FOOD"
    MENU = "MENU"
    DESSERT = "DESSERT"

class Meal(db.Model):
    __tablename__ = "Meals"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), unique=False, nullable=False)
    price = Column(Integer, unique=False, nullable=False, default=0)
    calories = Column(Integer, unique=False, nullable=False, default=0)
    image_url = Column(String(255), unique=False, nullable=True)
    description = Column(String(255), unique=False, nullable=True)
    stars = Column(Integer, unique=False, nullable=False, default=0)
    type = Column(sqla_Enum(MealType), unique=False, nullable=False, default=MealType.FOOD)

    def __repr__(self):
        return f"<Meal {self.id} ({self.name})>"

    @staticmethod
    def get_all(limit_per_type: Optional[int] = 0) -> list[Self]:
        if limit_per_type and int(limit_per_type) > 0:
            MealAlias = aliased(Meal)
            
            subquery = (
                select(MealAlias.id)
                .where(MealAlias.type == Meal.type)
                .order_by(MealAlias.type, MealAlias.id)
                .limit(limit_per_type)
                .correlate(Meal)
            )

            query = (
                select(Meal)
                .where(Meal.id.in_(subquery))
                .order_by(Meal.type, Meal.id)
            )

            return db.session.execute(query).scalars().all()

        return db.session.query(Meal).all()
        
    @staticmethod
    def get_all_by_ids(ids: list[int]) -> list[Self]:
        return db.session.query(Meal).filter(Meal.id.in_(ids)).all()

    @staticmethod
    def get_all_by_type(meal_type: MealType) -> list[Self]:
        meals = db.session.query(Meal).filter_by(type=meal_type).all()
        return meals

    def get_fallback_image_url(self, url_root: str) -> Optional[str]:
        match self.type:
            case MealType.BEVERAGE:
                return url_root + "static/fallback/beverage.jpg"
            case MealType.MENU:
                return url_root + "static/fallback/menu.jpg"
            case MealType.FOOD:
                return url_root + "static/fallback/food.jpg"
            case MealType.DESSERT:
                return url_root + "static/fallback/dessert.jpg"
            case _:
                return url_root + "static/fallback/menu.jpg"

    def to_dto(self) -> dict:
        image_url = str(self.image_url) if self.image_url else None
        has_image_url = bool(not self.image_url is None)
        if image_url and image_url.lower().startswith("/static/"):
            image_url = request.url_root + image_url.removeprefix("/")
        elif not image_url:
            image_url = self.get_fallback_image_url(request.url_root)
            
        return {
            "id": int(self.id),
            "name": str(self.name),
            "price": int(self.price),
            "calories": int(self.calories),
            "image_url": image_url,
            "has_image_url": has_image_url,
            "fallback_image_url": self.get_fallback_image_url(request.url_root),
            "description": str(self.description or "Ennek az ételnek vagy italnak nincs leírása, de biztosan nagyon finom."),
            "has_description": bool(not self.description is None),
            "stars": int(self.stars),
            "type": self.type,
            "is_free": bool(self.price == 0),
            "is_error": False,
            "display_price": f"{self.price} Ft"
        }

    @staticmethod
    def create(name: str, price: str = 0, calories: int = 0, image_url: Optional[str] = None, description: Optional[str] = None, stars: int = 0, type: Optional[MealType] = MealType.FOOD) -> Self:
        new_meal = None

        try:
            if not is_valid_enum_value(type, MealType):
                raise InvalidEnumValueException()

            price = validate_meal_price(price)
            calories = validate_meal_calories(calories)
            image_url = validate_image_url(image_url)
            description = validate_description(description)
            stars = validate_meal_stars(stars)

            new_meal = Meal(
                name=name,
                price=price,
                calories=calories,
                image_url=image_url,
                description=description,
                stars=stars,
                type=type,
            )

            db.session.add(new_meal)
            db.session.commit()

            db.session.refresh(new_meal)
            return new_meal
        except FlashedException as e:
            print(traceback.format_exc())
            db.session.rollback()
            raise MealCreationException(e.flash_message, e.css_class, e.http_code)

    @staticmethod
    def get_by_id_or_none(id: int) -> Optional[Self]:
        try:
            return db.session.query(Meal).filter_by(id=id).first()
        except:
            print(traceback.format_exc())
            return None
        
    @staticmethod
    def get_by_id_or_exception(id: int) -> Self:
        try:
            result = db.session.query(Meal).filter_by(id=id).first()
            if result is None:
                raise MealNotFoundException()
            
            return result
        except:
            print(traceback.format_exc())
            raise MealNotFoundException()
        
    def delete(self) -> None:
        db.session.delete(self)
        db.session.commit()

    def update_from_dict(self, values: dict) -> Self:
        commit_changes = False

        if "name" in values:
            self.name = values.get("name")
            commit_changes = True
        
        if "price" in values:
            self.price = validate_meal_price(values.get("price", None))
            commit_changes = True

        if "calories" in values:
            self.calories = validate_meal_calories(values.get("calories", None))
            commit_changes = True

        if "image_url" in values:
            self.image_url = validate_image_url(values.get("image_url", None))
            commit_changes = True

        if "description" in values:
            self.description = validate_description(values.get("description", None))
            commit_changes = True

        if "type" in values:
            self.type = str_to_enum_value(values.get("type", None), MealType) 
            commit_changes = True

        if commit_changes:
            db.session.add(self)
            db.session.commit()
        
        db.session.refresh(self)
        
        return self
        
class Order(db.Model):
    __tablename__ = "Orders"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, db.ForeignKey(User.id), unique=False, nullable=False)
    date_created = Column(DateTime, unique=False, nullable=False, default=lambda: datetime.now(timezone.utc))
    address = Column(String(255), unique=False, nullable=False)
    is_completed = Column(Boolean, unique=False, nullable=False, default=False)

    __table_args__ = (
        db.Index(
            "idx_user_id", "user_id"
        ),
    )

    def __repr__(self):
        return f"<Order {self.id} ({self.user_id})>"
    
    @staticmethod
    def get_by_id_or_none(id: int) -> Self | None:
        try:
            return db.session.query(Order).filter_by(id=id).first()
        except:
            print(traceback.format_exc())
            return None
        
    @staticmethod
    def get_by_id_or_exception(id: int) -> Self:
        try:
            result = db.session.query(Order).filter_by(id=id).first()
            if result is None:
                raise OrderNotFoundException()
            
            return result
        except:
            print(traceback.format_exc())
            raise OrderNotFoundException()

    @staticmethod
    def get_all() -> list[Self]:
        orders = db.session.query(Order).all()
        return orders
    
    @staticmethod
    def create(user_id: int, address: str) -> Self:
        try:
            user = User.get_by_id_or_none(user_id)
            if not user:
                raise UserNotFoundException()

            address = validate_address(address)

            new_order = Order(
                user_id=user_id,
                address=address,
            )

            db.session.add(new_order)
            db.session.commit()
            db.session.refresh(new_order)

            return new_order
        except exc.IntegrityError:
            print(traceback.format_exc())
            db.session.rollback()
            raise OrderCreationException()
        
    def to_dto(self) -> dict:
        return {
            "id": int(self.id),
            "user_id": int(self.user_id),
            "date_created": f'{self.date_created.isoformat()}Z',
            "address": str(self.address),
            "is_completed": bool(self.is_completed),
            "is_error": False,
        }
    
    def set_is_completed(self, is_completed: bool) -> Self:
        self.is_completed = is_completed
        db.session.commit()
        db.session.refresh(self)
        return self
    
    def delete(self) -> None:
        db.session.delete(self)
        db.session.commit()

    def add_item(self, meal_id: int, quantity: Optional[int] = 1) -> "OrderItem":
        meal = Meal.get_by_id_or_none(meal_id)
        if not meal:
            raise MealNotFoundException()
        
        new_order_item = OrderItem.create(
            order_id=self.id,
            meal_id=meal_id,
            quantity=quantity,
        )

        return new_order_item
    
    def get_items(self) -> list["OrderItem"]:
        return OrderItem.get_by_order_id_or_none(self.id) or []
    
    def get_detailed_items(self) -> list[tuple["OrderItem", "Meal"]]:
        return db.session.query(OrderItem, Meal).join(Meal, OrderItem.meal_id == Meal.id).where(OrderItem.order_id == self.id).all()
    
    def get_all_by_user_id(user_id: int) -> list[Self]:
        orders = db.session.query(Order).filter_by(user_id=user_id).all()
        return orders
    
    def set_address(self, address: Optional[str]) -> Self:
        self.address = validate_address(
            address=address
        )

        db.session.commit()
        db.session.refresh(self)
        return self

class OrderItem(db.Model):
    __tablename__ = "OrderItems"

    order_id = Column(Integer, primary_key=True)
    meal_id = Column(Integer, primary_key=True)
    quantity = Column(Integer, unique=False, nullable=False, default=1)

    __table_args__ = (
        db.PrimaryKeyConstraint(
            order_id,
            meal_id,
        ),
    )

    def __repr__(self):
        return f"<OrderItem {self.order_id} ({self.meal_id})>"
    
    @staticmethod
    def get_by_order_id_or_none(order_id: int) -> list[Self]:
        try:
            return db.session.query(OrderItem).filter_by(order_id=order_id).all()
        except:
            print(traceback.format_exc())
            return []
    
    @staticmethod
    def get_by_id_or_none(order_id: int, meal_id: int) -> Self | None:
        try:
            return db.session.query(OrderItem).filter_by(order_id=order_id, meal_id=meal_id).first()
        except:
            print(traceback.format_exc())
            return []
        
    @staticmethod
    def get_by_id_or_exception(order_id: int, meal_id: int) -> Self:
        try:
            result = db.session.query(OrderItem).filter_by(order_id=order_id, meal_id=meal_id).first()
            if not result:
                raise OrderItemNotFoundException()
            
            return result
        except:
            print(traceback.format_exc())
            raise OrderItemNotFoundException()
    
    @staticmethod
    def create(order_id: int, meal_id: int, quantity: Optional[int] = 1) -> Self:
        if not order_id or not meal_id:
            raise InvalidPayloadException("Hiányos JSON mezők")
        
        try:
            order = Order.get_by_id_or_none(order_id)
            if not order:
                raise OrderNotFoundException()
            
            meal = Meal.get_by_id_or_none(meal_id)
            if not meal:
                raise MealNotFoundException()
            
            quantity = validate_quantity(quantity)

            new_order_item = OrderItem(
                order_id=order_id,
                meal_id=meal_id,
                quantity=quantity,
            )

            db.session.add(new_order_item)
            db.session.commit()
            db.session.refresh(new_order_item)

            return new_order_item
        except exc.IntegrityError:
            print(traceback.format_exc())
            db.session.rollback()
            raise OrderItemCreationException()
        
    def to_dto(self) -> dict:
        return {
            "order_id": int(self.order_id),
            "meal_id": int(self.meal_id),
            "quantity": int(self.quantity),
            "is_error": False,
        }
    
    def delete(self) -> None:
        db.session.delete(self)
        db.session.commit()

    def set_quantity(self, quantity: Optional[int]) -> Self:
        quantity = validate_quantity(quantity)
        self.quantity = quantity

        db.session.commit()
        db.session.refresh(self)
        return self