from dataclasses import dataclass
from typing import Tuple

# TODO: en este commit vamos a trabajar en el reconocimiento de las extensiones del archivo abierto


@dataclass(frozen=True)
class Extensions:
    PLAIN_TEXT: str = ".txt"
    ASSEMBLY: str = ".asm"
    C: str = ".c"
    C_PLUS_PLUS: str = ".cpp"
    C_SHARP: str = ".cs"
    CSS: str = ".css"
    HTML: str = ".html"
    JAVA: str = ".java"
    JAVASCRIPT: str = ".js"
    JSON: str = ".json"
    LUA: str = ".lua"
    LISP: str = ".lisp"
    EMACS_LISP: str = ".el"
    MATLAB: str = ".m"
    MARKDOWN: str = ".md"
    OCAML: str = ".ml"
    PHP: str = ".php"
    PYTHON: str = ".py"
    POWERSHELL: str = ".ps1"
    RUBY: str = ".rb"
    RUST: str = ".rs"
    R: str = ".r"
    SQL: str = ".sql"
    SWIFT: str = ".swift"
    SHELL: str = ".sh"
    SCALA: str = ".scala"
    TYPESCRIPT: str = ".ts"
    XML: str = ".xml"
    YAML: str = ".yaml"

    @staticmethod
    def get_available_extensions() -> Tuple[str]:
        return tuple(getattr(Extensions, field) for field in Extensions.__annotations__)
