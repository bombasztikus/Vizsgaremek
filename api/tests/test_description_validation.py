import pytest
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.validation import *
from src.exceptions import *

def test_normalization():
    assert validate_description("   asd abc   ") == "asd abc"

def test_none_is_considered_valid_input():
    assert validate_description(None) == None

def test_return_type():
    assert isinstance(validate_description("asd"), str)
    assert isinstance(validate_description(None), type(None))