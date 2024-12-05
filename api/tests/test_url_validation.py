import pytest
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.validation import *
from src.exceptions import *

def test_return_type():
    assert isinstance(validate_image_url("http://example.com"), str)
    assert isinstance(validate_image_url(None), type(None))

def test_normalization():
    assert validate_image_url("  http://example.com  ") == "http://example.com"
    assert validate_image_url("HtTpS://ExAmPLe.cOm  ") == "https://example.com"

def test_no_or_wrong_protocol():
    with pytest.raises(InvalidURLException):
        validate_image_url("example.com")
    with pytest.raises(InvalidURLException):
        validate_image_url("asd://example.com")
    with pytest.raises(InvalidURLException):
        validate_image_url("file://example.com")

def test_none_input_returns_none():
    assert validate_image_url(None) == None