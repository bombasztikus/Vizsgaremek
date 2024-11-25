from unittest import *
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.validation import *
from src.exceptions import *

class TestValidateMealPrice(TestCase):
    def price_is_none(self):
        with self.assertRaises(InvalidPriceException):
            validate_meal_price(None)

    def price_is_not_int(self):
        with self.assertRaises(InvalidPriceException):
            validate_meal_price("asd")

    def price_is_negative(self):
        with self.assertRaises(InvalidPriceException):
            validate_meal_price("-1")

    def price_is_valid(self):
        self.assertEqual(validate_meal_price("1"), 1)

if __name__ == '__main__':
    main()