from .models import User
from . import db
from flask import flash
from argon2 import PasswordHasher

ph = PasswordHasher()

def create_user(email: str, full_name: str, password: str, is_employee: bool = True) -> User | None:
    email = str(email).strip().lower()
    if 255 < len(email) or len(email) < 1 or "@" not in email:
        return flash("Érvénytelen email hossz", "error")

    full_name = str(full_name).strip()
    if 255 < len(full_name) or len(full_name) < 1:
        return flash("Érvénytelen név hossz", "error")

    password = str(password)
    if 255 < len(password) or len(password) < 1:
        return flash("Érvénytelen jelszó hossz", "error")

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