from dataclasses import dataclass
from typing import Dict, Final, List


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
