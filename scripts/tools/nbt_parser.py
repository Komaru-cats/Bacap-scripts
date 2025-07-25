import re
from typing import Union, Dict, List, Any

from .Color import Color
from .utils import cut_namespace


def is_decimal(num):
    pattern = re.compile(r"^-?\d+$")
    return re.search(pattern, num)


def nbt_decoder(input_str: str) -> Any:
    """
    Translate components to python types.
    :param input_str: Component.
    :return: Some python type (depends on input).
    """
    signature = {"'": "'", "\"": "\"", "{": "}", "[": "]"}

    def strip_key(key: str) -> str:
        return key.strip("'").strip("\"")

    def remove_escaping_in_string(string: str):
        return "\\".join((x.replace("\\", "") for x in string.split(r"\\")))

    def convert_type(value: str) -> Union[list, dict, str, bool, float, int]:
        if value.startswith("[") and value.endswith("]"):
            return parse_list(value)
        elif value.startswith("{") and value.endswith("}"):
            return parse_nbt(value)
        elif (value.startswith("'") and value.endswith("'")) or (value.startswith("\"") and value.endswith("\"")):
            value = value[1:-1]
            try:
                if value.startswith("{") and value.endswith("}"):
                    return parse_nbt(remove_escaping_in_string(value))
                elif value.startswith("[") and value.endswith("]"):
                    return parse_list(remove_escaping_in_string(value))
            except ValueError:
                pass
            return remove_escaping_in_string(value)
        elif value.endswith("b"):
            return bool(int(value[:-1]))
        elif value.lower() in ("false", "true"):
            return True if value == "true" else False
        elif value[-1] in ("f", "d"):
            return float(value[:-1])
        elif value[-1] in ("s",):
            return int(value[:-1])
        elif is_decimal(value):
            return int(value)
        else:
            raise ValueError(f"Undefined type: {value}")

    def parse_nbt(input_nbt):
        input_nbt = input_nbt[1:-1]
        result = {}
        current_key = ''
        current_value = ''
        in_key = True
        in_value = False
        brace_counter = 0
        current_quote = None
        is_escaping = False
        i = 0
        while i < len(input_nbt):
            char = input_nbt[i]
            if in_key:
                if char in signature.keys() and current_quote is None:
                    current_quote = char
                    brace_counter += 1
                    current_key += char
                elif char == signature.get(current_quote):
                    brace_counter -= 1
                    current_key += char
                    if brace_counter == 0:
                        current_quote = None
                elif char == ':' and current_quote is None:
                    current_key = cut_namespace(current_key)
                    in_key = False
                    in_value = True
                elif current_quote:
                    current_key += char
                elif char not in [",", " "]:
                    current_key += char
            elif in_value:
                if is_escaping:
                    current_value += char
                    is_escaping = False
                elif char == "\\":
                    current_value += char
                    is_escaping = True
                elif current_quote is None:
                    if char == " ":
                        pass
                    elif char == ",":
                        current_key = strip_key(current_key)
                        result[current_key] = convert_type(current_value)
                        current_key = ''
                        current_value = ''
                        in_key = True
                        in_value = False
                        current_quote = None
                    elif char in signature.keys():
                        current_quote = char
                        current_value += char
                        brace_counter += 1
                    else:
                        current_value += char
                elif char == signature[current_quote]:
                    current_value += char
                    brace_counter -= 1
                    if brace_counter == 0:
                        current_key = strip_key(current_key)
                        result[current_key] = convert_type(current_value)
                        current_key = ''
                        current_value = ''
                        in_key = True
                        in_value = False
                        current_quote = None
                elif char == current_quote:
                    current_value += char
                    brace_counter += 1
                else:
                    current_value += char
            i += 1
        if current_key:
            current_key = strip_key(current_key)
            result[current_key] = convert_type(current_value)
        return result

    def parse_list(value: str) -> list:
        value = value[1:-1]
        if not value:
            return []
        if value[1] == ";":
            value = value.partition(";")[2]
        result = []
        current_value = ''
        brace_counter = 0
        current_quote = None
        is_escaping = False
        i = 0
        while i < len(value):
            char = value[i]
            if is_escaping:
                current_value += char
                is_escaping = False
            elif char == "\\":
                current_value += char
                is_escaping = True
            elif current_quote is None:
                if char in signature.keys():
                    current_quote = char
                    brace_counter += 1
                    current_value += char
                elif char == "," and brace_counter == 0:
                    result.append(convert_type(current_value))
                    current_value = ''
                elif char not in [" ", ","]:
                    current_value += char
            elif char == signature[current_quote]:
                current_value += char
                brace_counter -= 1
                if brace_counter == 0:
                    current_quote = None
            elif char == current_quote:
                current_value += char
                brace_counter += 1
            else:
                current_value += char
            i += 1
        if current_value:
            result.append(convert_type(current_value))
        return result

    return convert_type(input_str)


def nbt_encoder(nbt: Dict | List | float | int | str) -> str:
    """
    Translate python types to mc nbt.
    Also, it works dirtily, because text-json components in mc hardcoded.
    :param nbt: Some python-type to convert.
    :return: Nbt (str).
    """

    def escape_string(value: str) -> str:
        return value.replace("'", "\\'").replace("\"", "\\\\\"")

    def convert_dict(data: dict) -> str:
        result = "{"
        for key, value in data.items():
            if isinstance(key, str):
                key = escape_string(key)
            result += f"{key}:{convert_value(value)},"
        if result.endswith(","):
            result = result[:-1]
        result += "}"
        return result

    def convert_list(data: List) -> str:
        result = ""
        types = []
        for value in data:
            types.append(type(value) is int)
            result += f"{convert_value(value)},"
        if result.endswith(","):
            result = result[:-1]
        if len(types) > 0 and all(types):
            result = f"[I;{result}]"
        else:
            result = f"[{result}]"
        return result

    def convert_string(value: str) -> str:
        return f"\"{escape_string(value)}\""

    def convert_int(value: int) -> str:
        return str(value)

    def convert_float(value: float) -> str:
        return f"{value}f"

    def convert_color(value: Color) -> str:
        return f"\"{escape_string(value.value)}\""

    def convert_bool(value: bool) -> str:
        return "true" if value else "false"

    def convert_value(value: Any) -> str:
        if isinstance(value, dict):
            return convert_dict(value)
        elif isinstance(value, list):
            return convert_list(value)
        elif isinstance(value, str):
            return convert_string(value)
        elif isinstance(value, Color):
            return convert_color(value)
        elif type(value) == int:
            return convert_int(value)
        elif isinstance(value, float):
            return convert_float(value)
        elif isinstance(value, bool):
            return convert_bool(value)
        else:
            raise TypeError(f"Unsupported data type: {type(value)}\n{nbt}")

    return convert_value(nbt)
