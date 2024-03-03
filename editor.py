from PySide6.QtCore import Slot, Qt
from PySide6.QtWidgets import QScrollBar, QTabWidget, QPlainTextEdit
from PySide6.QtGui import QColor, QFontDatabase
from theme import ThemeModes
from utils import get_circle


from PySide6.QtCore import QRegularExpression
from PySide6.QtGui import QTextCharFormat, QFont, QSyntaxHighlighter
from PySide6.QtGui import QKeyEvent


class PythonSyntaxHighlighter(QSyntaxHighlighter):
    def __init__(self, document):
        super().__init__(document)
        self.highlighting_rules = []
        class_format = QTextCharFormat()
        class_format.setFontWeight(QFont.Bold)
        class_format.setForeground(Qt.green)
        class_pattern = r"^\s*class\s+\w+\(.*$"
        function_format = QTextCharFormat()
        function_format.setFontItalic(True)
        function_format.setForeground(Qt.green)
        function_pattern = r"^\s*def\s+\w+\s*\(.*\)\s*:\s*$"
        comment_format = QTextCharFormat()
        comment_format.setBackground(QColor("#77ff77"))
        comment_pattern = r"^\s*#.*$"
        self.highlighting_rules.append((class_pattern, class_format))
        self.highlighting_rules.append((function_pattern, function_format))
        self.highlighting_rules.append((comment_pattern, comment_format))
        keyword_format = QTextCharFormat()
        keyword_format.setForeground(Qt.blue)
        keyword_format.setFontWeight(QFont.Bold)
        keywords = [
            "and",
            "as",
            "assert",
            "break",
            "class",
            "continue",
            "def",
            "del",
            "elif",
            "else",
            "except",
            "finally",
            "for",
            "from",
            "global",
            "if",
            "import",
            "in",
            "is",
            "lambda",
            "not",
            "or",
            "pass",
            "print",
            "raise",
            "return",
            "try",
            "while",
            "with",
            "yield",
            "int",
            "str",
            "bool",
            "float",
            "list",
            "set",
            "dict",
            "abs",
            "all",
            "any",
        ]
        for keyword in keywords:
            pattern = QRegularExpression(f"\\b{keyword}\\b")
            self.highlighting_rules.append((pattern, keyword_format))

    def highlightBlock(self, text):
        for pattern, format in self.highlighting_rules:
            expression = QRegularExpression(pattern)
            it = expression.globalMatch(text)
            while it.hasNext():
                match = it.next()
                self.setFormat(match.capturedStart(), match.capturedLength(), format)
        self.setCurrentBlockState(0)


class Editor(QPlainTextEdit):
    def __init__(self, parent=None):
        super().__init__()
        self._parent = parent
        self._has_changes = False
        self._is_open_mode = False
        self._scroll_bar = QScrollBar(self)
        self.highlighter = PythonSyntaxHighlighter(self.document())
        font = QFontDatabase.systemFont(QFontDatabase.FixedFont)
        self.setFont(font)
        self.setDocument(self.document())
        self.__configurate()

    @property
    def has_changes(self) -> bool:
        return self._has_changes

    @has_changes.setter
    def has_changes(self, value: bool) -> None:
        if not isinstance(value, bool):
            raise ValueError("value must be boolean")
        self._has_changes = value

    @property
    def is_open_mode(self) -> bool:
        return self._is_open_mode

    @is_open_mode.setter
    def is_open_mode(self, value: bool) -> None:
        self._is_open_mode = value

    @Slot()
    def on_change(self) -> None:
        # when open a file and placing content to the editor, doesn't count as change
        if self.is_open_mode:
            return
        self.has_changes = True
        parent = self.parentWidget()
        if parent is None:
            print("nothing to check")
            return
        related_tab = parent.parentWidget()
        if isinstance(related_tab, QTabWidget):
            related_tab.setTabIcon(
                related_tab.currentIndex(), get_circle(theme=ThemeModes.LIGHT)
            )
        else:
            raise TypeError("tab is not a QTabWidget")

    def __configurate(self) -> None:
        self.textChanged.connect(self.on_change)
        self.setUndoRedoEnabled(True)
        # self.setAcceptRichText(True)
        self.setVerticalScrollBar(self._scroll_bar)

    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key_Tab:
            self.insertPlainText("    ")  # Inserta 4 espacios
        else:
            super(Editor, self).keyPressEvent(event)
