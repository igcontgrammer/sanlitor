from abc import ABC, abstractmethod
from typing import List, Tuple

from PySide6.QtCore import QRegularExpression, Qt
from PySide6.QtGui import (QColor, QFont, QSyntaxHighlighter, QTextCharFormat,
                           QTextDocument)

from languages_keywords import Python


class HighlightFactory(ABC):
    @abstractmethod
    def set_syntax(self, document: QTextDocument):
        pass


# ************* C *************

# ************* C++ *************

# ************* C# *************

# ************* CSS *************

# ************* HTML *************

# ************* JAVA *************

# ************* JS *************

# ************* JSON *************


# ************* LUA *************

# ************* LISP *************

# ************* EMACS LISP *************

# ************* MATLAB *************

# ************* MARKDOWN *************

# ************* OCAML *************

# ************* PHP *************

# ************* PYTHON *************


class PythonSyntaxFactory(HighlightFactory):
    def set_syntax(self, document: QTextDocument):
        return PythonSyntaxHighlighter(document)


class PythonSyntaxHighlighter(QSyntaxHighlighter):
    def __init__(self, document: QTextDocument):
        super().__init__(document)
        self.highlighting_rules: List[Tuple[str, QTextCharFormat]] = []
        self._add_default_patterns()
        keyword_format = QTextCharFormat()
        keyword_format.setForeground(Qt.blue)
        keyword_format.setFontWeight(QFont.Bold)
        for keyword in Python.keywords:
            pattern = QRegularExpression(f"\\b{keyword}\\b")
            self.highlighting_rules.append((pattern, keyword_format))

    def _add_default_patterns(self):
        class_format = QTextCharFormat()
        class_format.setFontWeight(QFont.Bold)
        class_format.setForeground(Qt.black)
        class_pattern = QRegularExpression(r"^\s*class\s+\w+\(.*$")
        function_format = QTextCharFormat()
        function_format.setFontItalic(True)
        function_format.setForeground(Qt.blue)
        function_pattern = QRegularExpression(
            r"^\s*def\s+(\w+)\s*\((\s*\w+\s*:\s*\w+\s*(?:,\s*\w+\s*:\s*\w+\s*)*)\)\s*:\s*"
        )
        comment_format = QTextCharFormat()
        comment_format.setBackground(QColor("#77ff77"))
        comment_pattern = QRegularExpression(r"^\s*#.*$")
        self.highlighting_rules.append((class_pattern, class_format))
        self.highlighting_rules.append((function_pattern, function_format))
        self.highlighting_rules.append((comment_pattern, comment_format))

    def highlightBlock(self, text):
        for pattern, format in self.highlighting_rules:
            expression = QRegularExpression(pattern)
            it = expression.globalMatch(text)
            while it.hasNext():
                match = it.next()
                self.setFormat(match.capturedStart(), match.capturedLength(), format)
        self.setCurrentBlockState(0)


# ************* POWERSHELL *************


# ************* RUBY *************


# ************* RUST *************

# ************* R *************


# ************* SQL *************


# ************* SWIFT *************

# ************* SHELL *************

# ************* SCALA *************

# ************* TS *************

# ************* XML *************

# ************* YAML *************
