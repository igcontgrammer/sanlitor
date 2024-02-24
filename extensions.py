from dataclasses import dataclass
from typing import List


def available_extensions() -> List[str]:
    return [
        getattr(Extensions, attr)
        for attr in dir(Extensions)
        if not attr.startswith("__") and not callable(getattr(Extensions, attr))
    ]


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
