import pytest
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.validation import *
from src.exceptions import *

def test_price_is_none():
    with pytest.raises(InvalidPriceException):
        validate_meal_price(None)

def test_price_is_not_int():
    with pytest.raises(InvalidPriceException):
        validate_meal_price("asd")

def test_price_is_negative():
    with pytest.raises(InvalidPriceException):
        validate_meal_price("-1")

def test_price_is_valid():
    assert validate_meal_price("1") == 1

def test_return_type():
    assert isinstance(validate_meal_price("123"), int)