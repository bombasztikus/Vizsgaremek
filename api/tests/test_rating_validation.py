import pytest
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.validation import *
from src.exceptions import *

def test_return_type():
    assert isinstance(validate_meal_stars("1"), int)
    assert isinstance(validate_meal_stars(None), int)

def test_none_is_valid_input():
    assert validate_meal_stars(None) == 0

def test_invalid_int_as_input():
    with pytest.raises(InvalidStarsException):
        validate_meal_stars("asd")

    with pytest.raises(InvalidStarsException):
        validate_meal_stars("123")

    with pytest.raises(InvalidStarsException):
        validate_meal_stars("-1")

    with pytest.raises(InvalidStarsException):
        validate_meal_stars("6")

