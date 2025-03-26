from typing import Optional
from .exceptions import *

def validate_meal_price(price: Optional[str]) -> int:
    if price is None or price.strip() == "":
        raise InvalidPriceException()
    
    try:
        price = int(price)
    except ValueError:
        raise InvalidPriceException()

    if price < 0:
        raise InvalidPriceException()
    
    return price

def validate_meal_calories(calories: Optional[str]) -> int:
    if not calories:
        raise InvalidCaloriesException()

    try:
        calories = int(calories)
    except ValueError:
        raise InvalidCaloriesException()
    
    if calories < 0:
        raise InvalidCaloriesException()
    if calories > 100_000:
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

    if 255 < len(email) or len(email) < 3 or "@" not in email:
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

    if 255 < len(password) or len(password) < 6:
        raise InvalidPasswordException("Érvénytelen jelszó hossz")
    
    return password

def validate_address(address: Optional[str]) -> str:
    if not address:
        raise InvalidAddressException("Hiányzó cím")
    
    address = str(address).strip()

    if 255 < len(address) or len(address) < 1:
        raise InvalidAddressException("Érvénytelen cím hossz")
    
    return address

def validate_quantity(quantity: Optional[str]) -> int:
    if not quantity:
        raise InvalidQuantityException("Hiányzó mennyiség")
    
    try:
        quantity = int(quantity)
    except ValueError:
        raise InvalidQuantityException()
    
    if quantity < 1 or 100 < quantity:
        raise InvalidQuantityException("Érvénytelen mennyiség")
    
    return quantity

def validate_dto_or_exception(dto: dict, fields: dict) -> dict:
    """
    Leellenőrzi, hogy a dto tartalmazza-e az összes kötelező mezőt.
    fields formátuma:
    {
        "field_name": ExceptionType,
    }
    """

    for field, exception in fields.items():
        if not field in dto:
            raise exception
        
    return dto