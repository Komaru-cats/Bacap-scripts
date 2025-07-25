import sys
from difflib import get_close_matches
from typing import *
from functools import wraps

literal_color_list = Literal["black", "red", "green", "yellow", "blue", "purple", "cyan", "white"]


def get_formatting(color: str = "white", bold: bool = False, italic: bool = False) -> str:
    """
    Format string using ANSI.
    """
    font_dict = {
        "bold": "1",
        "italic": "3"
    }
    color_dict = {
        "black": "30",
        "red": "31",
        "green": "32",
        "yellow": "33",
        "blue": "34",
        "purple": "35",
        "cyan": "36",
        "white": ""
    }
    bold = f"\033[{font_dict['bold']}m" if bold else ""
    italic = f"\033[{font_dict['italic']}m" if italic else ""
    color_code = f"\033[{color_dict[color]}m" if color else ""
    return color_code + bold + italic


class Icon:
    """
    Class for creating Icon with formating.
    Contains correct len and __str__ function.
    """
    basic = None
    warning = None
    error = None
    input = None

    def __init__(self, icon: str, color: literal_color_list = "white", bold: bool = False, italic: bool = False):
        self.icon = get_formatting(color, bold, italic) + icon

    def __str__(self):
        return self.icon

    def __add__(self, other):
        return str(self) + str(other)

    def __radd__(self, other):
        return str(other) + str(self)

    def __len__(self):
        return len(self.icon)


Icon.basic = Icon("[i]", "purple", True)
Icon.warning = Icon("[!]", "yellow", True)
Icon.error = Icon("[e]", "red", True)
Icon.input = Icon("[>]", "green")


class EmptyInputError(Exception):
    """Exception to exit from input"""
    pass


def exit_on_empty_input(func):
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            return result
        except EmptyInputError:
            return

    return wrapper


class Interface:
    """
    Class for work with console input and output.
    It can format types (color_type_data param).
    Contain function to get and print some configurable values.
    """

    def __init__(self, default_color: literal_color_list = "white",
                 default_bold: bool = False, default_italic: bool = False, output_icon: str = Icon.basic,
                 input_icon: str = Icon.input, format_type_data: Dict[Type, Dict[str, str | bool]] = None):
        """
        Initializes a new instance of the Interface class.
        :param default_color: Default color.
        :param default_bold: Default Bold.
        :param default_italic: Default Italic.
        :param output_icon: Icon instance for base output icon. 
        :param input_icon: Icon instance for base input icon.
        :param format_type_data: The dict with config of formatting.
        Key is a Type (ex. int), value is dict with keys: color, bold, italic.
        """
        self.default_color = default_color
        self.default_bold = default_bold
        self.default_italic = default_italic
        self.output_icon = output_icon
        self.input_icon = input_icon
        self.format_type_data = format_type_data

    def __get_text_properties(self, data, color=None, bold=None, italic=None) -> Tuple[str, bool, bool]:
        data_type_params = None
        if self.format_type_data:
            data_type_params = self.format_type_data.get(type(data))
        if color is None:
            if data_type_params:
                color = data_type_params["color"]
            else:
                color = self.default_color
        if bold is None:
            if data_type_params:
                bold = data_type_params["bold"]
            else:
                bold = self.default_bold
        if italic is None:
            if data_type_params:
                italic = data_type_params["italic"]
            else:
                italic = self.default_italic
        return color, bold, italic

    def text_wrapper(self, data: Any, color: literal_color_list = None, bold: bool = None, italic: bool = None) -> str:
        """
        Format value with format_type_data and return styled text.
        :param data: Any data.
        :param color: Color to override base color for this type.
        :param bold: Bold to override base color for this type.
        :param italic: Italic to override base color for this type.
        :return: String with formating.
        """
        color, bold, italic = self.__get_text_properties(data, color, bold, italic)
        return "\033[0m" + get_formatting(color, bold, italic) + str(data)

    def text_list_to_text(self, text_list: Iterable, separator: str = "\n"):
        return separator.join((self.text_wrapper(text) for text in text_list))

    def output(self, data: Any, color: literal_color_list = None, bold: bool = None, italic: bool = None,
               icon: Icon = None, indent: int = 0):
        """
        Output any data and use style-settings to output this.
        :param data: Any value.
        :param color: Add color to text.
        :param bold: Make text bold.
        :param italic: Make text italic.
        :param icon: Icon instance for base input icon.
        Allow you to set custom.
        If None, the default input_icon from self.
        :param indent: The amount of space to print msg.
        :return: None
        """
        icon = icon or self.output_icon
        if isinstance(data, str) and len(data.splitlines()) > 1:
            lines = data.splitlines()
            lines_without_first = [(" " * (len(icon) + indent + 1) + self.text_wrapper(line, color, bold, italic)) for
                                   line in lines[1:]]
            text = self.text_wrapper(lines[0], color, bold, italic) + "\n" + "\n".join(lines_without_first)
        else:
            text = self.text_wrapper(data, color, bold, italic)
        sys.stdout.write(" " * indent + icon + " " + text + "\n\33[0m")

    def get_value(self, msg: str, value_type: Type | Callable = None, possible_value: Iterable = None,
                  indent: int = 0, icon: Icon = None, function_to_check: Callable = None,
                  print_close: bool = True, close_n: int = 3, exit_on_empty: bool = False) -> Any | str | int:
        """
        Accept msg and value settings to get and return configured or not value.
        :param msg: The message to console.
        :param value_type: Accept type or function to convert value.
        Except ValueError and get input again.
        :param possible_value: The iterable object of possible values.
        If value isn't in one, get input again.
        :param indent: The amount of space to print msg.
        :param icon: Icon instance for base input icon.
        Allow you to set custom.
        If None, the default input_icon from self.
        :param function_to_check: The function to check value.
        If this function with input value doesn't raise ValueError, return value.
        :param print_close: If True and possible_values set, print close variants if input not in one.
        :param close_n: The Amount of variant for print_close.
        :param exit_on_empty: Exit the function, there this one called, need @exit_on_empty_input
        :return: User's input.
        Can be Any value.
        Depends on value_type.
        """
        if possible_value:
            possible_value_text = set(map(str, possible_value))
        else:
            possible_value_text = ()
        if len(msg.splitlines()) > 1:
            lines = msg.splitlines()
            lines_without_first = [(" " * (len(icon) + indent + 1) + line) for line in lines[1:]]
            msg = lines[0] + "\n" + "\n".join(lines_without_first)
        icon = icon or self.input_icon
        while True:
            value = input(" " * indent + icon + " " + msg + " " + "\33[0m")
            if exit_on_empty and value == "":
                raise EmptyInputError
            if value_type:
                try:
                    value = value_type(value)
                except ValueError:
                    continue
            if possible_value:
                if value not in possible_value:
                    if print_close:
                        variants = get_close_matches(str(value), possible_value_text, close_n, cutoff=0.2)
                        if variants:
                            self.output("Close possible: " + ", ".join(variants), indent=indent)
                    continue
            if function_to_check:
                if not function_to_check(value):
                    continue
            break
        return value

    def get_bool(self, msg, indent: int = 0, icon: Icon = None, true_values: Iterable | str = None,
                 false_values: Iterable | str = None, exit_on_empty: bool = False) -> bool:
        """
        Like get_value, but can only return bool and contains default values.
        :param msg: The message to console.
        :param indent: The amount of space to print msg.
        :param icon: Icon instance for base input icon.
        :param true_values: Iterable[str] or str of values to get true.
        :param false_values: Iterable[str] or str of values to get false.
        :param exit_on_empty: Exit the function, there this one called, need @exit_on_empty_input
        :return: bool
        """
        icon = icon or self.input_icon
        if len(msg.splitlines()) > 1:
            lines = msg.splitlines()
            lines_without_first = [(" " * (len(icon) + indent + 1) + line) for line in lines[1:]]
            msg = lines[0] + "\n" + "\n".join(lines_without_first)

        true_values = true_values or ("1", "true", "yes", "t", "y")
        false_values = false_values or ("0", "false", "no", "f", "n")
        if isinstance(true_values, str):
            while True:
                value = input(" " * indent + icon + " " + msg + " " + "\33[0m").lower()
                if exit_on_empty and value == "":
                    raise EmptyInputError
                if value == true_values:
                    return True
                elif value == false_values:
                    return False
        else:
            while True:
                value = input(" " * indent + icon + " " + msg + " " + "\33[0m").lower()
                if exit_on_empty and value == "":
                    raise EmptyInputError
                if value in true_values:
                    return True
                elif value in false_values:
                    return False

    def get_value_from_variants(self, msg: str, indent: int = 0, icon: Icon = None,
                                exit_on_empty: bool = False, **kwargs: Dict[str, str]) -> Any:
        """
        Return value from kwargs
        :param msg: The message to console.
        :param indent: The amount of space to print msg
        :param icon: Icon instance for base input icon.
        :param exit_on_empty: Exit the function, there this one called, need @exit_on_empty_input
        :param kwargs: Key is what need to input, value is what value will be returned.
        :return: Value from kwargs
        """
        icon = icon or self.input_icon
        msg = " " * indent + icon + " " + msg + " " + "\33[0m"
        while True:
            value = input(msg)
            if exit_on_empty and value == "":
                raise EmptyInputError
            if value in kwargs.keys():
                return kwargs[value]


class MenuInterface:
    """
    Class for creating a console menu.
    Contain decorators to create a menu and auto-creating msg to input functions.
    """

    def __init__(self, loop: bool = True, input_icon: Icon = Icon.input, func_separator: str = " | ",
                 show_tips: bool = True, tips_separator: str = "/", to_exit: str = ""):
        """

        :param loop: It True, Menu closed only when to_exit will be inputted.
        :param input_icon: Icon instance for base input icon.
        :param func_separator: Separator for function's names in msg.
        :param show_tips: Does show keys, what can be input.
        :param tips_separator: Separator for function's keys in msg.
        :param to_exit: String for exit from loop.
        """
        self._class_obj = None
        self.funcs_menu = {}
        self.loop = loop
        self.input_icon = input_icon
        self.func_separator = func_separator
        self.show_tips = show_tips
        self.tips_separator = tips_separator
        self.to_exit = to_exit

    def register_func(self, name: str, key: str):
        """
        Registering function for a menu.
        :param name: Name of function in msg.
        :param key: Key to input for call.
        """

        def decorator(func: Callable) -> Callable:
            self.funcs_menu[key] = {
                "name": name,
                "func": func,
            }

            @wraps(func)
            def wrapper(*args, **kwargs) -> None:
                return func(*args, **kwargs)

            return wrapper

        return decorator

    def register_class(self) -> Callable:
        """
        Registering class for a menu.
        """

        def decorator(cls) -> Type:
            self._class_obj = cls()
            return cls

        return decorator

    def menu(self, *args, **kwargs):
        """
        Run a menu
        """
        if len(self.funcs_menu) == 0:
            raise ValueError("Can't find registered functions")
        names = self.func_separator.join((func_data["name"] for func_data in self.funcs_menu.values()))
        tips = self.tips_separator.join(self.funcs_menu.keys())
        while self.loop:
            key = input(self.input_icon + " " + names + f" [{tips}]: " + "\33[0m")
            if key == self.to_exit:
                break
            if key in self.funcs_menu.keys():
                if self._class_obj:
                    self.funcs_menu[key]["func"](self._class_obj, *args, **kwargs)
                else:
                    self.funcs_menu[key]["func"](*args, **kwargs)


def func_loop(func: Callable):
    """
    Decorator for create function loop.
    If the function returns True, loop breaks.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        while True:
            result = func(*args, **kwargs)
            if result:
                return result

    return wrapper
