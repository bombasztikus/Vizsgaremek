class UserCreationException(Exception):
    def __init__(self, flash_message: str = "Ismeretlen hiba", css_class: str = "danger", *args: object) -> None:
        super().__init__(*args)
        self.flash_message = flash_message
        self.css_class = css_class