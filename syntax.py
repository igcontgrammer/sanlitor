from typing import Tuple


class Syntax:

    def __init__(self, selected_language: str = "Plain Text"):
        self._selected_language = selected_language

    def set_syntax(self):
        print(f"Setting the {self._selected_language} syntax...")
