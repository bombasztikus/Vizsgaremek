from typing import Self
import flask_login
import enum
from src.exceptions import *
from sqlalchemy import exc
from . import db
from argon2 import PasswordHasher
from argon2 import exceptions as ph_exc

ph = PasswordHasher()

class User(db.Model, flask_login.UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    full_name = db.Column(db.String(255), unique=False, nullable=False)
    is_employee = db.Column(db.Boolean, unique=False, nullable=False, default=False)
    password = db.Column(db.String(255), unique=False, nullable=False)

    def __repr__(self):
        return f"<User {self.id} ({self.email})>"
    
    @staticmethod  
    def get_by_id(id: int) -> Self | None:
        try:
            return db.session.query(User).filter_by(id=id).first()
        except:
            return None
    
    @staticmethod
    def create(email: str, full_name: str, password: str, is_employee: bool = True) -> Self:
        try:
            email = str(email).strip().lower()
            if 255 < len(email) or len(email) < 1 or "@" not in email:
                raise UserCreationException("Érvénytelen email hossz")
            
            email_exists = db.session.query(User.email).filter_by(email=email).scalar()
            if email_exists:
                raise UserCreationException("Az email cím már használatban van")

            full_name = str(full_name).strip()
            if 255 < len(full_name) or len(full_name) < 1:
                raise UserCreationException("Érvénytelen név hossz")

            password = str(password)
            if 255 < len(password) or len(password) < 1:
                raise UserCreationException("Érvénytelen jelszó hossz")

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
        try:
            email = str(email).strip().lower()
            user = db.session.query(User).filter_by(email=email).first()

            if not user:
                raise UserNotFoundException()
            
            password_valid = ph.verify(user.password, password)
            if not password_valid:
                raise InvalidCredentialsException()

            return user
        except ph_exc.VerificationError:
            raise InvalidCredentialsException()
        
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return not self.is_authenticated()

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

class MealType(str, enum.Enum):
    BEVERAGE = "BEVERAGE"
    FOOD = "FOOD"
    MENU = "MENU"

class Meal(db.Model, flask_login.UserMixin):
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
        try:
            meals = db.session.query(Meal).all()
            return meals
        except exc.SQLAlchemyError as e:
            print(e._message)
            return []

    @staticmethod
    def get_all_by_type(meal_type: MealType) -> list[Self]:
        try:
            meals = db.session.query(Meal).filter_by(type=meal_type).all()
            return meals
        except exc.SQLAlchemyError as e:
            print(e._message)
            return []
        
    def to_dto(self) -> dict:
        return {
            "id": int(self.id),
            "name": str(self.name),
            "price": str(self.price),
            "currency": str(self.currency),
            "calories": int(self.calories),
            "image_url": str(self.image_url) if self.image_url else None,
            "description": str(self.description) if self.description else None,
            "stars": int(self.stars),
            "type": self.type,
            "is_free": bool(str(self.price) == "0"),
            "is_error": False,
        }