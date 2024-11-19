from typing import Optional
from .exceptions import *

def validate_meal_price(price: Optional[str]) -> int:
    if not price:
        raise InvalidPriceException()
    
    try:
        price = int(price)
    except ValueError:
        raise InvalidPriceException()

    if price < 0:
        raise InvalidPriceException()
    
    return price
    
def validate_currency(currency: Optional[str]) -> str:
    if not currency:
        raise InvalidCurrencyException()
    
    currency = currency.upper().strip()

    if len(str(currency)) != 3:
        raise InvalidCurrencyException()
    
    return currency

def validate_meal_calories(calories: Optional[str]) -> int:
    if not calories:
        InvalidCaloriesException()

    try:
        calories = int(calories)
    except ValueError:
        raise InvalidCaloriesException()
    
    if calories < 0:
        raise InvalidCaloriesException()
    
    return calories
    
def validate_image_url(image_url: Optional[str]) -> Optional[str]:
    if not image_url:
        return None
    
    image_url = str(image_url).lower().strip()
    
    if not (image_url.startswith("http://") or image_url.startswith("https://")):
        raise InvalidURLException("Érvénytelen illusztráció URL (hiányzó protokol: http:// vagy https://)")
        
    return image_url


def validate_description(description: Optional[str]) -> Optional[str]:
    if not description:
        return None
    
    return description.strip()

def validate_meal_stars(stars: Optional[str]) -> int:
    if not stars:
        return 0
    
    try:
        stars = int(stars)
    except ValueError:
        raise InvalidStarsException()
    
    min_stars = 0
    max_stars = 5
    if stars < min_stars or stars > max_stars:
        raise InvalidStarsException(f"Érvénytelen értékelés szám (legalább {min_stars} és legfeljebb {max_stars} lehet)")
    
    return stars
    
def validate_email(email: Optional[str]) -> str:
    if not email:
        raise InvalidEmailException("Hiányzó email cím")

    email = str(email).strip().lower()

    if 255 < len(email) or len(email) < 1 or "@" not in email:
        raise InvalidEmailException("Érvénytelen email hossz")
    
    return email
    
def validate_full_name(full_name: Optional[str]) -> str:
    if not full_name:
        raise InvalidFullNameException("Hiányzó név")
    
    full_name = str(full_name).strip()

    if 255 < len(full_name) or len(full_name) < 1:
        raise InvalidFullNameException("Érvénytelen név hossz")
    
    return full_name
    
def validate_password(password: Optional[str]) -> str:
    if not password:
        raise InvalidPasswordException("Hiányzó jelszó")
    
    password = str(password)

    if 255 < len(password) or len(password) < 1:
        raise InvalidPasswordException("Érvénytelen jelszó hossz")
    
    return password