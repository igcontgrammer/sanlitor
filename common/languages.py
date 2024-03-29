from dataclasses import dataclass


@dataclass(frozen=True)
class Languages:
    PLAIN_TEXT: str = "Plain Text"
    ASSEMBLY: str = "Assembly"
    C: str = "C"
    C_PLUS_PLUS: str = "C++"
    C_SHARP: str = "C#"
    CSS: str = "CSS"
    HTML: str = "HTML"
    JAVA: str = "Java"
    JAVASCRIPT: str = "JavaScript"
    JSON: str = "JSON"
    LUA: str = "Lua"
    LISP: str = "Lisp"
    EMACS_LISP: str = "Emacs Lisp"
    MATLAB: str = "Matlab"
    MARKDOWN: str = "Markdown"
    OCAML: str = "Ocaml"
    PHP: str = "PHP"
    PYTHON: str = "Python"
    POWERSHELL: str = "PowerShell"
    RUBY: str = "Ruby"
    RUST: str = "Rust"
    R: str = "R"
    SQL: str = "SQL"
    SWIFT: str = "Swift"
    SHELL: str = "Shell"
    SCALA: str = "Scala"
    TYPESCRIPT: str = "TypeScript"
    XML: str = "XML"
    YAML: str = "YAML"
