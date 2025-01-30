import pytest
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.validation import *
from src.exceptions import *

def test_calories_are_none():
    with pytest.raises(InvalidCaloriesException):
        validate_meal_calories(None)

def test_calories_arent_int():
    with pytest.raises(InvalidCaloriesException):
        validate_meal_calories("asd")

def test_calories_are_negative():
    with pytest.raises(InvalidCaloriesException):
        validate_meal_calories("-1")

def test_return_type():
    assert isinstance(validate_meal_calories("123"), int)

def test_calories_are_too_big():
    with pytest.raises(InvalidCaloriesException):
        validate_meal_calories("100001")

def test_calories_overflow():
    with pytest.raises(InvalidCaloriesException):
        validate_meal_calories("9999999999999999999")