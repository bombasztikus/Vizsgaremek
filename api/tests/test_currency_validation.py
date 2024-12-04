import pytest
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.validation import *
from src.exceptions import *

def test_currency_is_none():
    with pytest.raises(InvalidCurrencyException):
        validate_currency(None)

def test_invalid_currency_len():
    with pytest.raises(InvalidCurrencyException):
        validate_currency("a")

    with pytest.raises(InvalidCurrencyException):
        validate_currency("aaaa")

    with pytest.raises(InvalidCurrencyException):
        validate_currency("")

def test_currency_normalization():
    assert validate_currency("huf") == "HUF"
    assert validate_currency("   huf   ") == "HUF"
    assert validate_currency("HUF") == "HUF"

def test_return_type():
    assert isinstance(validate_currency("huf"), str)