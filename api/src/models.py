from typing import Optional, Self
import enum
from src.exceptions import *
from sqlalchemy import exc
from flask import request
from src.utils import is_valid_enum_value
from src.validation import *
from . import db
from argon2 import PasswordHasher
from argon2 import exceptions as ph_exc

ph = PasswordHasher()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    full_name = db.Column(db.String(255), unique=False, nullable=False)
    is_employee = db.Column(db.Boolean, unique=False, nullable=False, default=False)
    password = db.Column(db.String(255), unique=False, nullable=False)

    def __repr__(self):
        return f"<User {self.id} ({self.email})>"
    
    @staticmethod  
    def get_by_id_or_none(id: int) -> Self | None:
        try:
            return db.session.query(User).filter_by(id=id).first()
        except:
            return None
    
    @staticmethod
    def create(email: str, full_name: str, password: str, is_employee: bool = True) -> Self:
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
            db.session.rollback()
            raise UserCreationException()
    
    @staticmethod
    def verify(email: str, password: str) -> Self:
        if not email or not password:
            raise InvalidPayloadException("Hiányos JSON mezők")

        try:
            email = str(email).strip().lower()
            user = db.session.query(User).filter_by(email=email).first()

            if not user:
                raise InvalidCredentialsException()
            
            password_valid = ph.verify(user.password, password)
            if not password_valid:
                raise InvalidCredentialsException()

            return user
        except ph_exc.VerificationError:
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

class MealType(str, enum.Enum):
    BEVERAGE = "BEVERAGE"
    FOOD = "FOOD"
    MENU = "MENU"
    DESSERT = "DESSERT"

class Meal(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), unique=False, nullable=False)
    price = db.Column(db.String(255), unique=False, nullable=False, default="0")
    currency = db.Column(db.String(3), unique=False, nullable=False, default="HUF")
    calories = db.Column(db.Integer, unique=False, nullable=False, default=0)
    image_url = db.Column(db.String(255), unique=False, nullable=True)
    description = db.Column(db.String(255), unique=False, nullable=True)
    stars = db.Column(db.Integer, unique=False, nullable=False, default=0)
    type = db.Column(db.Enum(MealType), unique=False, nullable=False, default=MealType.FOOD)

    def __repr__(self):
        return f"<Meal {self.id} ({self.name})>"

    @staticmethod
    def get_all() -> list[Self]:
        meals = db.session.query(Meal).all()
        return meals

    @staticmethod
    def get_all_by_type(meal_type: MealType) -> list[Self]:
        meals = db.session.query(Meal).filter_by(type=meal_type).all()
        return meals
        
    def to_dto(self) -> dict:
        image_url = str(self.image_url) if self.image_url else None
        if image_url and image_url.lower().startswith("/static/"):
            image_url = request.url_root + image_url.removeprefix("/")
        elif not image_url:
            if self.type == MealType.BEVERAGE:
                image_url = request.url_root + "static/fallback/beverage.jpg"
            elif self.type == MealType.MENU or self.type == MealType.DESSERT:
                image_url = request.url_root + "static/fallback/menu.jpg"
            elif self.type == MealType.FOOD:
                image_url = request.url_root + "static/fallback/food.jpg"
            
        return {
            "id": int(self.id),
            "name": str(self.name),
            "price": str(self.price),
            "currency": str(self.currency),
            "calories": int(self.calories),
            "image_url": image_url,
            "description": str(self.description) if self.description else None,
            "stars": int(self.stars),
            "type": self.type,
            "is_free": bool(str(self.price) == "0"),
            "is_error": False,
        }
        
    @staticmethod
    def create(name: str, price: str = "0", currency: str = "HUF", calories: int = 0, image_url: Optional[str] = None, description: Optional[str] = None, stars: int = 0, type: Optional[MealType] = MealType.FOOD) -> Self:
        new_meal = None

        try:
            if not is_valid_enum_value(type, MealType):
                raise InvalidEnumValueException()

            price = validate_meal_price(price)
            currency = validate_currency(currency)
            calories = validate_meal_calories(calories)
            image_url = validate_image_url(image_url)
            description = validate_description(description)
            stars = validate_meal_stars(stars)

            new_meal = Meal(
                name=name,
                price=price,
                currency=currency,
                calories=calories,
                image_url=image_url,
                description=description,
                stars=stars,
                type=type,
            )

            db.session.add(new_meal)
            db.session.commit()

            return new_meal
        except FlashedException as e:
            db.session.rollback()
            raise MealCreationException(e.flash_message, e.css_class, e.http_code)
            
        finally:
            db.session.refresh(new_meal)
            return new_meal