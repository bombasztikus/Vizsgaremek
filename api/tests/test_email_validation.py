import pytest
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.validation import *
from src.exceptions import *

def test_return_type():
    assert isinstance(validate_email("jsmith@example.com"), str)

def test_normalization():
    assert validate_email("  jsmith@eXaMpLe.COM  ") == "jsmith@example.com"

def test_none_is_not_accepted():
    with pytest.raises(InvalidEmailException):
        validate_email(None)

def test_email_over_realistic_limit():
    with pytest.raises(InvalidEmailException):
        email = "".join("x" for _ in range(256))
        validate_email(email)

def test_email_too_short_or_omits_at_symbol():
    with pytest.raises(InvalidEmailException):
        validate_email("")

    with pytest.raises(InvalidEmailException):
        validate_email("ab")