from typing import Final, Tuple, Dict
from . import QMenu, QAction, Slot, ActionHelper, SectionsNames
from common.languages import Languages
from syntax import Syntax


class LanguageMenu(QMenu):

    def __init__(self):
        super().__init__()
        self._language_menu = QMenu(SectionsNames.LANGUAGE)
        self._languages_actions = self._get_languages_actions()
        self.__create_languages_menus()
        self.__create_languages_actions()

    @property
    def menu(self) -> QMenu:
        return self._language_menu

    _LANGUAGES_OPTIONS: Final[Dict[str, Tuple[str]]] = {
        "C": (Languages.C, Languages.C_PLUS_PLUS, Languages.C_SHARP, Languages.CSS),
        "J": (Languages.JAVA, Languages.JAVASCRIPT, Languages.JSON),
        "L": (Languages.LUA, Languages.LISP, Languages.EMACS_LISP),
        "M": (Languages.MARKDOWN, Languages.MATLAB),
        "P": (Languages.PHP, Languages.PYTHON, Languages.POWERSHELL),
        "R": (Languages.RUBY, Languages.RUST, Languages.R),
        "S": (Languages.SQL, Languages.SWIFT, Languages.SHELL, Languages.SCALA),
    }

    def _get_languages_actions(self) -> Dict[str, QAction]:
        return {
            Languages.PLAIN_TEXT: self._add_plain_text_action,
            Languages.ASSEMBLY: self._get_assembly_action,
            Languages.C: self._get_c_action,
            Languages.C_PLUS_PLUS: self._get_c_plus_plus_action,
            Languages.C_SHARP: self._get_c_sharp_action,
            Languages.CSS: self._get_css_action,
            Languages.JAVA: self._get_java_action,
            Languages.JAVASCRIPT: self._get_js_action,
            Languages.JSON: self._get_json_action,
            Languages.LUA: self._get_lua_action,
            Languages.LISP: self._get_lisp_action,
            Languages.EMACS_LISP: self._get_elisp_action,
            Languages.MATLAB: self._get_matlab_action,
            Languages.PHP: self._get_php_action,
            Languages.PYTHON: self._get_python_action,
            Languages.POWERSHELL: self._get_powershell_action,
            Languages.RUBY: self._get_ruby_action,
            Languages.RUST: self._get_rust_action,
            Languages.R: self._get_r_action,
            Languages.SQL: self._get_sql_action,
            Languages.SWIFT: self._get_swift_action,
            Languages.SHELL: self._get_shell_action,
            Languages.SCALA: self._get_scala_action,
            Languages.TYPESCRIPT: self._get_typescript_action,
            Languages.XML: self._get_xml_action,
            Languages.YAML: self._add_yaml_action,
            Languages.OCAML: self._add_ocaml_action,
        }

    def __create_languages_menus(self) -> None:
        self._add_plain_text_action()
        self._add_assembly_action()
        self._add_languages_options_actions()
        self._add_html_action()
        self._add_ocaml_action()
        self._add_typescript_action()
        self._add_xml_action()
        self._add_yaml_action()

    def _add_languages_options_actions(self) -> None:
        for name in self._LANGUAGES_OPTIONS.keys():
            menu = QMenu(name)
            self._language_menu.addMenu(menu)

    def __create_languages_actions(self) -> None:
        for language_key, languages in self._LANGUAGES_OPTIONS.items():
            for action in self._language_menu.actions():
                if action.text() == language_key:
                    for language in languages:
                        language_action = QAction(language, self)
                        ActionHelper().config(
                            action=language_action,
                            shortcut="",
                            status_tip=f"Select {language} language",
                            method=self._languages_actions.get(language),
                        )
                        action.menu().addAction(language_action)

    def _get_xml_action(self) -> None:
        select_xml_action = QAction(Languages.XML, self)
        ActionHelper().config(
            action=select_xml_action,
            shortcut="",
            status_tip="Select XML language",
            method=self._set_XML,
        )
        return select_xml_action

    def _add_xml_action(self) -> None:
        self._language_menu.addAction(self._get_xml_action())

    def _add_plain_text_action(self) -> None:
        select_plain_text_action = QAction(Languages.PLAIN_TEXT, self)
        ActionHelper().config(
            action=select_plain_text_action,
            shortcut="",
            status_tip="Select Plain Text language",
            method=self._set_plain_text,
        )
        self._language_menu.addAction(select_plain_text_action)

    def _add_typescript_action(self) -> None:
        select_typescript_action = QAction(Languages.TYPESCRIPT, self)
        ActionHelper().config(
            action=select_typescript_action,
            shortcut="",
            status_tip="Select TypeScript language",
            method=self._set_typescript,
        )
        self._language_menu.addAction(select_typescript_action)

    def _add_yaml_action(self) -> None:
        select_yaml_action = QAction(Languages.YAML, self)
        ActionHelper().config(
            action=select_yaml_action,
            shortcut="",
            status_tip="Select YAML language",
            method=self._set_YAML,
        )
        self._language_menu.addAction(select_yaml_action)

    def _add_ocaml_action(self) -> None:
        select_ocaml_action = QAction(Languages.OCAML, self)
        ActionHelper().config(
            action=select_ocaml_action,
            shortcut="",
            status_tip="Select OCaml language",
            method=self._set_ocaml,
        )
        self._language_menu.addAction(select_ocaml_action)

    def _add_assembly_action(self) -> None:
        self._language_menu.addAction(self._get_assembly_action())

    def _get_assembly_action(self) -> QAction:
        set_assembly_action = QAction(Languages.ASSEMBLY, self)
        ActionHelper().config(
            action=set_assembly_action,
            shortcut="",
            status_tip="Select Assembly language",
            method=self._set_assembly,
        )
        return set_assembly_action

    def _get_c_action(self) -> QAction:
        set_c_action = QAction(Languages.C, self)
        ActionHelper().config(
            action=set_c_action,
            shortcut="",
            status_tip="Select C language",
            method=self._set_c(),
        )
        return set_c_action

    def _get_c_plus_plus_action(self) -> QAction:
        set_c_plus_plus_action = QAction(Languages.C_PLUS_PLUS, self)
        ActionHelper().config(
            action=set_c_plus_plus_action,
            shortcut="",
            status_tip="Select C++ language",
            method=self._set_plus_plus(),
        )
        return set_c_plus_plus_action

    def _get_c_sharp_action(self) -> QAction:
        set_c_sharp_action = QAction(Languages.C_SHARP, self)
        ActionHelper().config(
            action=set_c_sharp_action,
            shortcut="",
            status_tip="Select C# language",
            method=self._set_c_sharp(),
        )
        return set_c_sharp_action

    def _get_css_action(self) -> QAction:
        set_css_action = QAction(Languages.CSS, self)
        ActionHelper().config(
            action=set_css_action,
            shortcut="",
            status_tip="Select CSS language",
            method=self._set_css(),
        )
        return set_css_action

    def _get_java_action(self) -> QAction:
        set_java_action = QAction(Languages.JAVA, self)
        ActionHelper().config(
            action=set_java_action,
            shortcut="",
            status_tip="Select Java language",
            method=self._set_java(),
        )
        return set_java_action

    def _get_js_action(self) -> QAction:
        set_js_action = QAction(Languages.JAVASCRIPT, self)
        ActionHelper().config(
            action=set_js_action,
            shortcut="",
            status_tip="Select JavaScript language",
            method=self._set_js(),
        )
        return set_js_action

    def _get_json_action(self) -> QAction:
        set_json_action = QAction(Languages.JSON, self)
        ActionHelper().config(
            action=set_json_action,
            shortcut="",
            status_tip="Select JSON language",
            method=self._set_json(),
        )
        return set_json_action

    def _get_lua_action(self) -> QAction:
        set_lua_action = QAction(Languages.LUA, self)
        ActionHelper().config(
            action=set_lua_action,
            shortcut="",
            status_tip="Select Lua language",
            method=self._set_lua(),
        )
        return set_lua_action

    def _get_lisp_action(self) -> QAction:
        set_lisp_action = QAction(Languages.LISP, self)
        ActionHelper().config(
            action=set_lisp_action,
            shortcut="",
            status_tip="Select Lisp language",
            method=self._set_lisp(),
        )
        return set_lisp_action

    def _get_elisp_action(self) -> QAction:
        set_elisp_action = QAction(Languages.EMACS_LISP, self)
        ActionHelper().config(
            action=set_elisp_action,
            shortcut="",
            status_tip="Select Emacs Lisp language",
            method=self._set_elisp(),
        )
        return set_elisp_action

    def _add_html_action(self) -> None:
        set_html_action = QAction(Languages.HTML, self)
        ActionHelper().config(
            action=set_html_action,
            shortcut="",
            status_tip="Select HTML language",
            method=self._set_html,
        )
        self._language_menu.addAction(set_html_action)

    def _get_markdown_action(self) -> QAction:
        set_markdown_action = QAction(Languages.MARKDOWN, self)
        ActionHelper().config(
            action=set_markdown_action,
            shortcut="",
            status_tip="Select Markdown language",
            method=self._set_markdown(),
        )
        return set_markdown_action

    def _get_matlab_action(self) -> QAction:
        set_matlab_action = QAction(Languages.MATLAB, self)
        ActionHelper().config(
            action=set_matlab_action,
            shortcut="",
            status_tip="Select Matlab language",
            method=self._set_matlab(),
        )
        return set_matlab_action

    def _get_php_action(self) -> QAction:
        set_php_action = QAction(Languages.PHP, self)
        ActionHelper().config(
            action=set_php_action,
            shortcut="",
            status_tip="Select PHP language",
            method=self._set_php(),
        )
        return set_php_action

    def _get_python_action(self) -> QAction:
        set_python_action = QAction(Languages.PYTHON, self)
        ActionHelper().config(
            action=set_python_action,
            shortcut="",
            status_tip="Select Python language",
            method=self._set_python(),
        )
        return set_python_action

    def _get_powershell_action(self) -> QAction:
        set_powershell_action = QAction(Languages.POWERSHELL, self)
        ActionHelper().config(
            action=set_powershell_action,
            shortcut="",
            status_tip="Select PowerShell language",
            method=self._set_powershell(),
        )
        return set_powershell_action

    def _get_ruby_action(self) -> QAction:
        set_ruby_action = QAction(Languages.RUBY, self)
        ActionHelper().config(
            action=set_ruby_action,
            shortcut="",
            status_tip="Select Ruby language",
            method=self._set_ruby(),
        )
        return set_ruby_action

    def _get_rust_action(self) -> QAction:
        set_rust_action = QAction(Languages.RUST, self)
        ActionHelper().config(
            action=set_rust_action,
            shortcut="",
            status_tip="Select Rust language",
            method=self._set_rust(),
        )
        return set_rust_action

    def _get_r_action(self) -> QAction:
        set_r_action = QAction(Languages.R, self)
        ActionHelper().config(
            action=set_r_action,
            shortcut="",
            status_tip="Select R language",
            method=self._set_r(),
        )
        return set_r_action

    def _get_sql_action(self) -> QAction:
        set_sql_action = QAction(Languages.SQL, self)
        ActionHelper().config(
            action=set_sql_action,
            shortcut="",
            status_tip="Select SQL language",
            method=self._set_sql(),
        )
        return set_sql_action

    def _get_swift_action(self) -> QAction:
        set_swift_action = QAction(Languages.SWIFT, self)
        ActionHelper().config(
            action=set_swift_action,
            shortcut="",
            status_tip="Select Swift language",
            method=self._set_swift(),
        )
        return set_swift_action

    def _get_shell_action(self) -> QAction:
        set_shell_action = QAction(Languages.SHELL, self)
        ActionHelper().config(
            action=set_shell_action,
            shortcut="",
            status_tip="Select Shell language",
            method=self._set_shell(),
        )
        return set_shell_action

    def _get_scala_action(self) -> QAction:
        set_scala_action = QAction(Languages.SCALA, self)
        ActionHelper().config(
            action=set_scala_action,
            shortcut="",
            status_tip="Select Scala language",
            method=self._set_scala(),
        )
        return set_scala_action

    def _get_typescript_action(self) -> QAction:
        set_typescript_action = QAction(Languages.TYPESCRIPT, self)
        ActionHelper().config(
            action=set_typescript_action,
            shortcut="",
            status_tip="Select TypeScript language",
            method=self._set_typescript,
        )
        return set_typescript_action

    @Slot()
    def _set_plain_text(self) -> None:
        print("Plain Text")
        pass

    @Slot()
    def _set_assembly(self) -> None:
        print("Assembly")
        pass

    @Slot()
    def _set_c(self) -> None:
        print("C")
        pass

    @Slot()
    def _set_plus_plus(self) -> None:
        print("C++")
        pass

    @Slot()
    def _set_c_sharp(self) -> None:
        print("C#")
        pass

    @Slot()
    def _set_css(self) -> None:
        print("CSS")
        pass

    @Slot()
    def _set_java(self) -> None:
        print("Java")
        pass

    @Slot()
    def _set_js(self) -> None:
        print("JavaScript")
        pass

    @Slot()
    def _set_json(self) -> None:
        print("JSON")
        pass

    @Slot()
    def _set_lua(self) -> None:
        print("Lua")
        pass

    @Slot()
    def _set_lisp(self) -> None:
        print("Lisp")
        pass

    @Slot()
    def _set_elisp(self) -> None:
        print("Emacs Lisp")
        pass

    @Slot()
    def _set_html(self) -> None:
        print("HTML")
        pass

    @Slot()
    def _set_markdown(self) -> None:
        print("Markdown")
        pass

    @Slot()
    def _set_matlab(self) -> None:
        print("Matlab")
        pass

    @Slot()
    def _set_php(self) -> None:
        print("PHP")
        pass

    @Slot()
    def _set_python(self) -> None:
        print("Python")
        pass

    @Slot()
    def _set_powershell(self) -> None:
        print("PowerShell")
        pass

    @Slot()
    def _set_ruby(self) -> None:
        print("Ruby")
        pass

    @Slot()
    def _set_rust(self) -> None:
        print("Rust")
        pass

    @Slot()
    def _set_r(self) -> None:
        print("R")
        pass

    @Slot()
    def _set_sql(self) -> None:
        print("SQL")
        pass

    @Slot()
    def _set_swift(self) -> None:
        print("Swift")
        pass

    @Slot()
    def _set_shell(self) -> None:
        print("Shell")
        pass

    @Slot()
    def _set_scala(self) -> None:
        print("Scala")
        pass

    @Slot()
    def _set_typescript(self) -> None:
        print("TypeScript")
        pass

    @Slot()
    def _set_XML(self) -> None:
        print("XML")
        pass

    @Slot()
    def _set_typescript(self) -> None:
        print("TypeScript")
        pass

    @Slot()
    def _set_YAML(self) -> None:
        print("YAML")
        pass

    @Slot()
    def _set_ocaml(self) -> None:
        print("OCaml")
        pass
