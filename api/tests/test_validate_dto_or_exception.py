import pytest
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.validation import *
from src.exceptions import *

def test_missing_field():
    with pytest.raises(InvalidEmailException):
        validate_dto_or_exception(
            dto={},
            fields={
            "email": InvalidEmailException("Az email cím megadása kötelező")
        })

def test_field_is_present():
    assert validate_dto_or_exception(
        dto={"email": "something"},
        fields={
            "email": InvalidEmailException("Az email cím megadása kötelező")
        }
    ) == {"email": "something"}

def test_multiple_fields():
    with pytest.raises(InvalidEmailException):
        validate_dto_or_exception(
            dto={},
            fields={
                "email": InvalidEmailException("Az email cím megadása kötelező"),
                "password": InvalidPasswordException("A jelszó megadása kötelező")
            }
        )

def test_multiple_fields_present():
    assert validate_dto_or_exception(
        dto={"email": "something", "password": "something"},
        fields={
            "email": InvalidEmailException("Az email cím megadása kötelező"),
            "password": InvalidPasswordException("A jelszó megadása kötelező")
        }
    ) == {"email": "something", "password": "something"}

def test_multiple_fields_present_but_one_missing():
    with pytest.raises(InvalidPasswordException):
        validate_dto_or_exception(
            dto={"email": "something"},
            fields={
                "email": InvalidEmailException("Az email cím megadása kötelező"),
                "password": InvalidPasswordException("A jelszó megadása kötelező")
            }
        )

def test_no_fields():
    assert validate_dto_or_exception(
        dto={},
        fields={}
    ) == {}