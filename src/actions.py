from sqlalchemy import exc
from .models import User
from . import db
from flask import flash
from argon2 import PasswordHasher

ph = PasswordHasher()

def create_user(email: str, full_name: str, password: str, is_employee: bool = True) -> User | None:
    try:
        email = str(email).strip().lower()
        if 255 < len(email) or len(email) < 1 or "@" not in email:
            return flash("Érvénytelen email hossz", "danger")
        
        email_exists = db.session.query(User.id).filter_by(email=email).scalar()
        if email_exists:
            return flash("Az email cím már használatban van", "danger")

        full_name = str(full_name).strip()
        if 255 < len(full_name) or len(full_name) < 1:
            return flash("Érvénytelen név hossz", "danger")

        password = str(password)
        if 255 < len(password) or len(password) < 1:
            return flash("Érvénytelen jelszó hossz", "danger")

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
        return None