from dataclasses import dataclass
from typing import Final


@dataclass(frozen=True)
class Languages:
    PLAIN_TEXT: Final[str] = "Plain Text"
    ASSEMBLY: Final[str] = "Assembly"
    C: Final[str] = "C"
    C_PLUS_PLUS: Final[str] = "C++"
    C_SHARP: Final[str] = "C#"
    CSS: Final[str] = "CSS"
    HTML: Final[str] = "HTML"
    JAVA: Final[str] = "Java"
    JAVASCRIPT: Final[str] = "JavaScript"
    JSON: Final[str] = "JSON"
    LUA: Final[str] = "Lua"
    LISP: Final[str] = "Lisp"
    EMACS_LISP: Final[str] = "Emacs Lisp"
    MATLAB: Final[str] = "Matlab"
    MARKDOWN: Final[str] = "Markdown"
    OCAML: Final[str] = "Ocaml"
    PHP: Final[str] = "PHP"
    PYTHON: Final[str] = "Python"
    POWERSHELL: Final[str] = "PowerShell"
    RUBY: Final[str] = "Ruby"
    RUST: Final[str] = "Rust"
    R: Final[str] = "R"
    SQL: Final[str] = "SQL"
    SWIFT: Final[str] = "Swift"
    SHELL: Final[str] = "Shell"
    SCALA: Final[str] = "Scala"
    TYPESCRIPT: Final[str] = "TypeScript"
    XML: Final[str] = "XML"
    YAML: Final[str] = "YAML"