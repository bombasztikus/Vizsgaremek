class FlashedException(Exception):
    def __init__(self, flash_message: str = "Ismeretlen hiba", css_class: str = "danger", http_code: int = 500, error_code: str = "unknown_error", *args: object) -> None:
        super().__init__(*args)
        self.flash_message = flash_message
        self.css_class = css_class
        self.http_code = http_code
        self.error_code = error_code

    def to_dto(self) -> dict:
        return {
        "error": self.flash_message,
        "css_class": self.css_class,
        "http_code": self.http_code,
        "is_error": True,
        "error_code": self.error_code
    }

class UserCreationException(FlashedException):
    def __init__(self, flash_message: str = "Ismeretlen hiba történt a fiók létrehozása közben", css_class: str = "danger", http_code: int = 500, error_code: str = "account_creation_error", *args: object) -> None:
        super().__init__(flash_message, css_class, http_code, error_code, *args)

class InvalidCredentialsException(FlashedException):
    def __init__(self, flash_message: str = "Érvénytelen bejelentkezési adatok", css_class: str = "warning", http_code: int = 401, error_code: str = "invalid_credentials", *args: object) -> None:
        super().__init__(flash_message, css_class, http_code, error_code, *args)

class NotFoundException(FlashedException):
    def __init__(self, flash_message: str = "A kért tartalom nem található", css_class: str = "warning", http_code: int = 404, error_code: str = "not_found", *args: object) -> None:
        super().__init__(flash_message, css_class, http_code, error_code, *args)

class UserNotFoundException(NotFoundException):
    def __init__(self, flash_message: str = "A felhasználó nem található", error_code: str = "user_not_found", *args: object) -> None:
        super().__init__(flash_message, error_code=error_code, *args)

class InvalidUserIDException(FlashedException):
    def __init__(self, flash_message = "Érvénytelen felhasználó azonosító", css_class = "danger", http_code = 422, error_code: str = "invalid_user_id", *args):
        super().__init__(flash_message, css_class, http_code, error_code, *args)

class InvalidEnumValueException(FlashedException):
    def __init__(self, flash_message: str = "Az érték nem egyezik az elfogadott értékek egyikével sem", css_class: str = "danger", http_code: int = 422, error_code: str = "invalid_enum_value", *args: object) -> None:
        super().__init__(flash_message, css_class, http_code, error_code, *args)

class InvalidPriceException(FlashedException):
    def __init__(self, flash_message: str = "Érvénytelen ár vagy egyéb pénzösszeg", css_class: str = "danger", http_code: int = 422, error_code: str = "invalid_price", *args: object) -> None:
        super().__init__(flash_message, css_class, http_code, error_code, *args)

class MealCreationException(FlashedException):
    def __init__(self, flash_message: str = "Ismeretlen hiba történt a termék létrehozása közben", css_class: str = "danger", http_code: int = 500, error_code: str = "meal_creation_error", *args: object) -> None:
        super().__init__(flash_message, css_class, http_code, error_code, *args)

class InvalidCurrencyException(FlashedException):
    def __init__(self, flash_message: str = "Érvénytelen valuta (valószínűleg nem követi az ISO 4217-es betű szabványt)", css_class: str = "danger", http_code: int = 422, error_code: str = "invalid_currency", *args: object) -> None:
        super().__init__(flash_message, css_class, http_code, error_code, *args)

class InvalidCaloriesException(FlashedException):
    def __init__(self, flash_message: str = "Érvénytelen kalória érték", css_class: str = "danger", http_code: int = 422, error_code: str = "invalid_calories", *args: object) -> None:
        super().__init__(flash_message, css_class, http_code, error_code, *args)

class InvalidURLException(FlashedException):
    def __init__(self, flash_message: str = "Érvénytelen URL", css_class: str = "danger", http_code: int = 422, error_code: str = "invalid_url", *args: object) -> None:
        super().__init__(flash_message, css_class, http_code, error_code, *args)

class InvalidStarsException(FlashedException):
    def __init__(self, flash_message: str = "Érvénytelen értékelés szám", css_class: str = "danger", http_code: int = 422, error_code: str = "invalid_stars", *args: object) -> None:
        super().__init__(flash_message, css_class, http_code, error_code, *args)

class UnauthorizedException(FlashedException):
    def __init__(self, flash_message: str = "Nem rendelkezel a kért tartalom eléréséhez szükséges jogosultságokkal", css_class: str = "danger", http_code: int = 403, error_code: str = "unauthorized", *args: object) -> None:
        super().__init__(flash_message, css_class, http_code, error_code, *args)

class EmailUnavailableException(FlashedException):
    def __init__(self, flash_message: str = "Az email cím nem használható", css_class: str = "danger", http_code: int = 409, error_code: str = "email_unavailable", *args: object) -> None:
        super().__init__(flash_message, css_class, http_code, error_code, *args)