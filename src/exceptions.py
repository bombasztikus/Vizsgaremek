class FlashedException(Exception):
    def __init__(self, flash_message: str = "Ismeretlen hiba", css_class: str = "danger", http_code: int = 500, *args: object) -> None:
        super().__init__(*args)
        self.flash_message = flash_message
        self.css_class = css_class
        self.http_code = http_code

class UserCreationException(FlashedException):
    def __init__(self, flash_message: str = "Ismeretlen hiba történt a fiók létrehozása közben", css_class: str = "danger", http_code: int = 400, *args: object) -> None:
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
    def __init__(self, flash_message = "Érvénytelen felhasználó azonosító", css_class = "danger", http_code = 400, *args):
        super().__init__(flash_message, css_class, http_code, *args)