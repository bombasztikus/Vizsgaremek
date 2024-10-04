from typing import Self
import flask_login

from src.exceptions import *
from sqlalchemy import exc
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
            user = db.sesion.query(User.email).filter_by(email=email).first()

            if not user:
                raise UserNotFoundException()
            
            # ez magától is dob exceptiont
            password_valid = ph.verify(user.password, password)

            return user
        except ph_exc.VerificationError:
            raise InvalidCredentialsException()
        
class SessionUser(flask_login.UserMixin):
    def __init__(
            self,
            id: str,
            email: str,
            is_authenticated: bool = False,
            is_active: bool = True,
            is_anonymous: bool = False,
    ) -> None:
        super().__init__()
        self.id = str(id)
        self.email = email
        self.is_authenticated = is_authenticated
        self.is_active = is_active
        self.is_anonymous = is_anonymous

    def get_id(self) -> str:
        return str(self.user_id)

    @staticmethod
    def get_by_id(id: str) -> User | None:
        user = User.get_by_id(id)
        if not user:
            return None
        
        return SessionUser.from_user(user)
    
    @staticmethod
    def from_user(user: User) -> Self:
        return SessionUser(
            id=user.id,
            email=user.email,
            is_authenticated=True,
            is_active=True,
            is_anonymous=False
        )