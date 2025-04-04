class APIException(Exception):
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

class UserCreationException(APIException):
    def __init__(self, flash_message: str = "Ismeretlen hiba történt a fiók létrehozása közben", css_class: str = "danger", http_code: int = 500, error_code: str = "account_creation_error", *args: object) -> None:
        super().__init__(flash_message, css_class, http_code, error_code, *args)

class InvalidCredentialsException(APIException):
    def __init__(self, flash_message: str = "Érvénytelen bejelentkezési adatok", css_class: str = "warning", http_code: int = 401, error_code: str = "invalid_credentials", *args: object) -> None:
        super().__init__(flash_message, css_class, http_code, error_code, *args)

class NotFoundException(APIException):
    def __init__(self, flash_message: str = "A kért tartalom nem található", css_class: str = "warning", http_code: int = 404, error_code: str = "not_found", *args: object) -> None:
        super().__init__(flash_message, css_class, http_code, error_code, *args)

class UserNotFoundException(NotFoundException):
    def __init__(self, flash_message: str = "A felhasználó nem található", error_code: str = "user_not_found", *args: object) -> None:
        super().__init__(flash_message, error_code=error_code, *args)

class InvalidUserIDException(APIException):
    def __init__(self, flash_message = "Érvénytelen felhasználó azonosító", css_class = "danger", http_code = 422, error_code: str = "invalid_user_id", *args):
        super().__init__(flash_message, css_class, http_code, error_code, *args)

class InvalidEnumValueException(APIException):
    def __init__(self, flash_message: str = "Az érték nem egyezik az elfogadott értékek egyikével sem", css_class: str = "danger", http_code: int = 422, error_code: str = "invalid_enum_value", *args: object) -> None:
        super().__init__(flash_message, css_class, http_code, error_code, *args)

class InvalidPriceException(APIException):
    def __init__(self, flash_message: str = "Érvénytelen ár vagy egyéb pénzösszeg", css_class: str = "danger", http_code: int = 422, error_code: str = "invalid_price", *args: object) -> None:
        super().__init__(flash_message, css_class, http_code, error_code, *args)

class MealCreationException(APIException):
    def __init__(self, flash_message: str = "Ismeretlen hiba történt a termék létrehozása közben", css_class: str = "danger", http_code: int = 500, error_code: str = "meal_creation_error", *args: object) -> None:
        super().__init__(flash_message, css_class, http_code, error_code, *args)

class InvalidCaloriesException(APIException):
    def __init__(self, flash_message: str = "Érvénytelen kalória érték", css_class: str = "danger", http_code: int = 422, error_code: str = "invalid_calories", *args: object) -> None:
        super().__init__(flash_message, css_class, http_code, error_code, *args)

class InvalidURLException(APIException):
    def __init__(self, flash_message: str = "Érvénytelen URL", css_class: str = "danger", http_code: int = 422, error_code: str = "invalid_url", *args: object) -> None:
        super().__init__(flash_message, css_class, http_code, error_code, *args)

class InvalidStarsException(APIException):
    def __init__(self, flash_message: str = "Érvénytelen értékelés szám", css_class: str = "danger", http_code: int = 422, error_code: str = "invalid_stars", *args: object) -> None:
        super().__init__(flash_message, css_class, http_code, error_code, *args)

class UnauthorizedException(APIException):
    def __init__(self, flash_message: str = "Nem rendelkezel a kért tartalom eléréséhez szükséges jogosultságokkal", css_class: str = "danger", http_code: int = 403, error_code: str = "unauthorized", *args: object) -> None:
        super().__init__(flash_message, css_class, http_code, error_code, *args)

class EmailUnavailableException(APIException):
    def __init__(self, flash_message: str = "Az email cím nem használható", css_class: str = "danger", http_code: int = 409, error_code: str = "email_unavailable", *args: object) -> None:
        super().__init__(flash_message, css_class, http_code, error_code, *args)

class InvalidPayloadException(APIException):
    def __init__(self, flash_message: str = "Érvénytelen kérés", css_class: str = "danger", http_code: int = 422, error_code: str = "invalid_payload", *args: object) -> None:
        super().__init__(flash_message, css_class, http_code, error_code, *args)

class InvalidEmailException(APIException):
    def __init__(self, flash_message: str = "Érvénytelen email cím", css_class: str = "danger", http_code: int = 400, error_code: str = "invalid_email", *args: object) -> None:
        super().__init__(flash_message, css_class, http_code, error_code, *args)

class InvalidFullNameException(APIException):
    def __init__(self, flash_message: str = "Érvénytelen név", css_class: str = "danger", http_code: int = 400, error_code: str = "invalid_full_name", *args: object) -> None:
        super().__init__(flash_message, css_class, http_code, error_code, *args)

class InvalidPasswordException(APIException):
    def __init__(self, flash_message: str = "Érvénytelen jelszó", css_class: str = "danger", http_code: int = 400, error_code: str = "invalid_password", *args: object) -> None:
        super().__init__(flash_message, css_class, http_code, error_code, *args)

class OrderCreationException(APIException):
    def __init__(self, flash_message: str = "Ismeretlen hiba történt a rendelés létrehozása közben", css_class: str = "danger", http_code: int = 500, error_code: str = "order_creation_error", *args: object) -> None:
        super().__init__(flash_message, css_class, http_code, error_code, *args)

class InvalidAddressException(APIException):
    def __init__(self, flash_message: str = "Érvénytelen cím", css_class: str = "danger", http_code: int = 422, error_code: str = "invalid_address", *args: object) -> None:
        super().__init__(flash_message, css_class, http_code, error_code, *args)

class OrderItemCreationException(APIException):
    def __init__(self, flash_message: str = "Ismeretlen hiba történt a rendelés elemének létrehozása közben", css_class: str = "danger", http_code: int = 500, error_code: str = "order_item_creation_error", *args: object) -> None:
        super().__init__(flash_message, css_class, http_code, error_code, *args)

class InvalidQuantityException(APIException):
    def __init__(self, flash_message: str = "Érvénytelen mennyiség", css_class: str = "danger", http_code: int = 422, error_code: str = "invalid_quantity", *args: object) -> None:
        super().__init__(flash_message, css_class, http_code, error_code, *args)

class OrderNotFoundException(NotFoundException):
    def __init__(self, flash_message: str = "A rendelés nem található", error_code: str = "order_not_found", *args: object) -> None:
        super().__init__(flash_message, error_code=error_code, *args)

class MealNotFoundException(NotFoundException):
    def __init__(self, flash_message: str = "A termék nem található", error_code: str = "meal_not_found", *args: object) -> None:
        super().__init__(flash_message, error_code=error_code, *args)

class InvalidOrderIDException(APIException):
    def __init__(self, flash_message = "Érvénytelen rendelés azonosító", css_class = "danger", http_code = 422, error_code: str = "invalid_order_id", *args):
        super().__init__(flash_message, css_class, http_code, error_code, *args)

class OrderItemNotFoundException(NotFoundException):
    def __init__(self, flash_message: str = "A rendelés eleme nem található", error_code: str = "order_item_not_found", *args: object) -> None:
        super().__init__(flash_message, error_code=error_code, *args)

class InvalidOrderItemIDException(APIException):
    def __init__(self, flash_message = "Érvénytelen rendelés elem azonosító", css_class = "danger", http_code = 422, error_code: str = "invalid_order_item_id", *args):
        super().__init__(flash_message, css_class, http_code, error_code, *args)

class InvalidMealIDException(APIException):
    def __init__(self, flash_message = "Érvénytelen termék azonosító", css_class = "danger", http_code = 422, error_code: str = "invalid_meal_id", *args):
        super().__init__(flash_message, css_class, http_code, error_code, *args)

class OrderItemUndeletableException(APIException):
    def __init__(self, flash_message = "A rendelés tétele nem törölhető", css_class = "warning", http_code = 409, error_code = "order_item_undeletable", *args):
        super().__init__(flash_message, css_class, http_code, error_code, *args)

class MealDeletionException(APIException):
    def __init__(self, flash_message: str = "Ismeretlen hiba történt a termék törlése közben", css_class: str = "danger", http_code: int = 500, error_code: str = "meal_deletion_error", *args: object) -> None:
        super().__init__(flash_message, css_class, http_code, error_code, *args)

class OrderItemCreationConflictException(APIException):
    def __init__(self, flash_message: str = "A tétel már létezik", css_class: str = "warning", http_code: int = 409, error_code: str = "order_item_creation_conflict", *args: object) -> None:
        super().__init__(flash_message, css_class, http_code, error_code, *args)