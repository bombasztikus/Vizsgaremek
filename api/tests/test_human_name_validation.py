import pytest
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.validation import *
from src.exceptions import *

def test_return_type():
    assert isinstance(validate_full_name("kis pista"), str)

def test_normalization():
    assert validate_full_name("  kis pista  ") == "kis pista"

def test_name_too_long():
    with pytest.raises(InvalidFullNameException):
        name = "".join("x" for _ in range(256))
        validate_full_name(name)

def test_name_too_short():
    with pytest.raises(InvalidFullNameException):
        validate_full_name("")

def test_none_is_not_allowed():
    with pytest.raises(InvalidFullNameException):
        validate_full_name(None)