import pytest
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.validation import *
from src.exceptions import *

def test_address_is_none():
    with pytest.raises(InvalidAddressException):
        validate_address(None)

def test_address_is_empty():
    with pytest.raises(InvalidAddressException):
        validate_address("")

def test_address_is_too_long():
    with pytest.raises(InvalidAddressException):
        validate_address("a" * 256)

def test_address_is_valid():
    assert validate_address("Test street 123") == "Test street 123"

def test_address_is_trimmed():
    assert validate_address("  Test street 123  ") == "Test street 123"
    assert validate_address("Test street 123  ") == "Test street 123"
    assert validate_address("  Test street 123") == "Test street 123"