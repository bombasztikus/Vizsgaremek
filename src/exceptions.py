class FlashedException(Exception):
    def __init__(self, flash_message: str = "Ismeretlen hiba", css_class: str = "danger", http_code: int = 500, *args: object) -> None:
        super().__init__(*args)
        self.flash_message = flash_message
        self.css_class = css_class
        self.http_code = http_code

    def to_dto(self) -> dict:
        return {
        "error": self.flash_message,
        "css_class": self.css_class,
        "http_code": self.http_code,
        "is_error": True,
    }

class UserCreationException(FlashedException):
    def __init__(self, flash_message: str = "Ismeretlen hiba történt a fiók létrehozása közben", css_class: str = "danger", http_code: int = 500, *args: object) -> None:
        super().__init__(flash_message, css_class, http_code, *args)

class InvalidCredentialsException(FlashedException):
    def __init__(self, flash_message: str = "Érvénytelen bejelentkezési adatok", css_class: str = "warning", http_code: int = 401, *args: object) -> None:
        super().__init__(flash_message, css_class, http_code, *args)

class NotFoundException(FlashedException):
    def __init__(self, flash_message: str = "A kért tartalom nem található", css_class: str = "warning", http_code: int = 404, *args: object) -> None:
        super().__init__(flash_message, css_class, http_code, *args)

class UserNotFoundException(NotFoundException):
    def __init__(self, flash_message: str = "A felhasználó nem található", *args: object) -> None:
        super().__init__(flash_message, *args)

class InvalidUserIDException(FlashedException):
    def __init__(self, flash_message = "Érvénytelen felhasználó azonosító", css_class = "danger", http_code = 422, *args):
        super().__init__(flash_message, css_class, http_code, *args)

class InvalidEnumValueException(FlashedException):
    def __init__(self, flash_message: str = "Az érték nem egyezik az elfogadott értékek egyikével sem", css_class: str = "danger", http_code: int = 422, *args: object) -> None:
        super().__init__(flash_message, css_class, http_code, *args)

class InvalidPriceException(FlashedException):
    def __init__(self, flash_message: str = "Érvénytelen ár vagy egyéb pénzösszeg", css_class: str = "danger", http_code: int = 422, *args: object) -> None:
        super().__init__(flash_message, css_class, http_code, *args)

class MealCreationException(FlashedException):
    def __init__(self, flash_message: str = "Ismeretlen hiba történt a termék létrehozása közben", css_class: str = "danger", http_code: int = 500, *args: object) -> None:
        super().__init__(flash_message, css_class, http_code, *args)

class InvalidCurrencyException(FlashedException):
    def __init__(self, flash_message: str = "Érvénytelen valuta (valószínűleg nem követi az ISO 4217-es betű szabványt)", css_class: str = "danger", http_code: int = 422, *args: object) -> None:
        super().__init__(flash_message, css_class, http_code, *args)

class InvalidCaloriesException(FlashedException):
    def __init__(self, flash_message: str = "Érvénytelen kalória érték", css_class: str = "danger", http_code: int = 422, *args: object) -> None:
        super().__init__(flash_message, css_class, http_code, *args)

class InvalidURLException(FlashedException):
    def __init__(self, flash_message: str = "Érvénytelen URL", css_class: str = "danger", http_code: int = 422, *args: object) -> None:
        super().__init__(flash_message, css_class, http_code, *args)

class InvalidStarsException(FlashedException):
    def __init__(self, flash_message: str = "Érvénytelen értékelés szám", css_class: str = "danger", http_code: int = 422, *args: object) -> None:
        super().__init__(flash_message, css_class, http_code, *args)

class UnauthorizedException(FlashedException):
    def __init__(self, flash_message: str = "Nem rendelkezel a kért tartalom eléréséhez szükséges jogosultságokkal", css_class: str = "danger", http_code: int = 403, *args: object) -> None:
        super().__init__(flash_message, css_class, http_code, *args)