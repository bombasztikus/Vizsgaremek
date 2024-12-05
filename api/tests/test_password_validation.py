import pytest
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.validation import *
from src.exceptions import *

def test_return_type():
    assert isinstance(validate_password("kispista"), str)

def test_input_is_untouched():
    test_str = "  kis pista  "
    assert validate_password(test_str) == test_str
    test_str2 = "AbC123"
    assert validate_password(test_str2) == test_str2

def test_name_too_long():
    with pytest.raises(InvalidPasswordException):
        name = "".join("x" for _ in range(256))
        validate_password(name)

def test_name_too_short():
    with pytest.raises(InvalidPasswordException):
        validate_password("")

def test_none_is_not_allowed():
    with pytest.raises(InvalidPasswordException):
        validate_password(None)