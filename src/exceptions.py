class FlashedException(Exception):
    def __init__(self, flash_message: str = "Ismeretlen hiba", css_class: str = "danger", *args: object) -> None:
        super().__init__(*args)
        self.flash_message = flash_message
        self.css_class = css_class

class UserCreationException(FlashedException):
    def __init__(self, flash_message: str = "Ismeretlen hiba történt a fiók létrehozása közben", css_class: str = "danger", *args: object) -> None:
        super().__init__(flash_message, css_class, *args)

class InvalidCredentialsException(FlashedException):
    def __init__(self, flash_message: str = "Érvénytelen bejelentkezési adatok", css_class: str = "warning", *args: object) -> None:
        super().__init__(flash_message, css_class, *args)

class UserNotFoundException(FlashedException):
    def __init__(self, flash_message: str = "A felhasználó nem található", css_class: str = "warning", *args: object) -> None:
        super().__init__(flash_message, css_class, *args)