from dataclasses import dataclass
from enum import Enum, auto
from typing import Dict, Final, List

# la lista de extensiones disponibles al momento de guardar un archivo


def available_extensions() -> List[str]:
    return [
        getattr(Extensions, attr)
        for attr in dir(Extensions)
        if not attr.startswith("__") and not callable(getattr(Extensions, attr))
    ]


def get_extensions_list() -> str:
    extensions = ""
    for key, value in EXTENSIONS_LIST.items():
        if key == "YAML":
            extensions += f"{key} {value}"
            break
        extensions += f"{key} {value};;"
    return extensions


EXTENSIONS_LIST: Final[Dict[str, str]] = {
    "Text Plain": "(*.txt)",
    "Assembly": "(*.asm)",
    "C": "(*.c)",
    "C++": "(*.cpp)",
    "C#": "(*.cs)",
    "CSS": "(*.css)",
    "HTML": "(*.html)",
    "Java": "(*.java)",
    "JavaScript": "(*.js)",
    "JSON": "(*.json)",
    "Lua": "(*.lua)",
    "Lisp": "(*.lisp)",
    "Emacs Lisp": "(*.el)",
    "Matlab": "(*.m)",
    "Markdown": "(*.md)",
    "OCaml": "(*.ml)",
    "PHP": "(*.php)",
    "Python": "(*.py)",
    "PowerShell": "(*.ps1)",
    "Ruby": "(*.rb)",
    "Rust": "(*.rs)",
    "R": "(*.r)",
    "SQL": "(*.sql)",
    "Swift": "(*.swift)",
    "Shell": "(*.sh)",
    "Scala": "(*.scala)",
    "TypeScript": "(*.ts)",
    "XML": "(*.xml)",
    "YAML": "(*.yaml)",
}


class LanguageSelected(Enum):
    TEXT_PLAIN = auto()
    ASSEMBLY = auto()
    C = auto()
    CPP = auto()
    CSHARP = auto()
    CSS = auto()
    HTML = auto()
    JAVA = auto()
    JAVASCRIPT = auto()
    JSON = auto()
    LUA = auto()
    LISP = auto()
    EMACS_LISP = auto()
    MATLAB = auto()
    MARKDOWN = auto()
    OCAML = auto()
    PHP = auto()
    PYTHON = auto()
    POWERSHELL = auto()
    RUBY = auto()
    RUST = auto()
    R = auto()
    SQL = auto()
    SWIFT = auto()
    SHELL = auto()
    SCALA = auto()
    TYPESCRIPT = auto()
    XML = auto()
    YAML = auto()


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


# Esto sirve para hacer mas dinamica la seleccion y posterior match de sintaxis del lenguaje seleccionado
EXTENSION_SELECTED: Final[Dict[str, LanguageSelected]] = {
    Extensions.PLAIN_TEXT: LanguageSelected.TEXT_PLAIN,
    Extensions.ASSEMBLY: LanguageSelected.ASSEMBLY,
    Extensions.C: LanguageSelected.C,
    Extensions.C_PLUS_PLUS: LanguageSelected.CPP,
    Extensions.C_SHARP: LanguageSelected.CSHARP,
    Extensions.CSS: LanguageSelected.CSS,
    Extensions.HTML: LanguageSelected.HTML,
    Extensions.JAVA: LanguageSelected.JAVA,
    Extensions.JAVASCRIPT: LanguageSelected.JAVASCRIPT,
    Extensions.JSON: LanguageSelected.JSON,
    Extensions.LUA: LanguageSelected.LUA,
    Extensions.LISP: LanguageSelected.LISP,
    Extensions.EMACS_LISP: LanguageSelected.EMACS_LISP,
    Extensions.MATLAB: LanguageSelected.MATLAB,
    Extensions.MARKDOWN: LanguageSelected.MARKDOWN,
    Extensions.OCAML: LanguageSelected.OCAML,
    Extensions.PHP: LanguageSelected.PHP,
    Extensions.PYTHON: LanguageSelected.PYTHON,
    Extensions.POWERSHELL: LanguageSelected.POWERSHELL,
    Extensions.RUBY: LanguageSelected.RUBY,
    Extensions.RUST: LanguageSelected.RUST,
    Extensions.R: LanguageSelected.R,
    Extensions.SQL: LanguageSelected.SQL,
    Extensions.SWIFT: LanguageSelected.SWIFT,
    Extensions.SHELL: LanguageSelected.SHELL,
    Extensions.SCALA: LanguageSelected.SCALA,
    Extensions.TYPESCRIPT: LanguageSelected.TYPESCRIPT,
    Extensions.XML: LanguageSelected.XML,
    Extensions.YAML: LanguageSelected.YAML,
}
