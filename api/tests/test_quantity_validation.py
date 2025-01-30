import pytest
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.validation import *
from src.exceptions import *

def test_quantity_is_none():
    with pytest.raises(InvalidQuantityException):
        validate_quantity(None)

def test_quantity_arent_int():
    with pytest.raises(InvalidQuantityException):
        validate_quantity("asd")

def test_quantity_are_negative():
    with pytest.raises(InvalidQuantityException):
        validate_quantity("-1")

def test_return_type():
    assert isinstance(validate_quantity("69"), int)

def test_quantity_are_too_big():
    with pytest.raises(InvalidQuantityException):
        validate_quantity("101")

def test_quantity_overflow():
    with pytest.raises(InvalidQuantityException):
        validate_quantity("9999999999999999999")

def test_quantity_is_valid():
    assert validate_quantity("1") == 1
    assert validate_quantity("100") == 100
    assert validate_quantity("50") == 50
    assert validate_quantity("10") == 10
    assert validate_quantity("5") == 5
