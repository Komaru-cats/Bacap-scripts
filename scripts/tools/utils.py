import json
import re
from pathlib import Path
from typing import *
from typing import Dict

from .Сonfig import Config

user_config = Config("user_config.json", can_object_change_config=False)


def cut_namespace(string_with_namespace: str) -> str:
    if ":" in string_with_namespace:
        return string_with_namespace.split(":", 1)[1]
    return string_with_namespace


def escape_quotes(text):
    return text.replace('\"', '\\\"')


def path_to_mc_path(file_path: Path) -> str:
    """
    :param file_path: Path to file
    :return: Path like in mc: relative, without backslashes and suffix.
    """
    parts = file_path.parts[3:]
    namespace = parts[0]
    return f"{namespace}:{"/".join(parts[2:]).partition(".")[0]}"


def mc_path_to_path(path_to_datapack: Path, typification: str, mcpath: str) -> Path:
    """
    :param path_to_datapack: Path to datapack folder.
    :param typification: McPath to some typification folder, like advancement
    :param mcpath: Path in mc: ex - "my_namespace:my_functions/my_function"
    :return: Path-object.
    """
    namespace, relative_path = mcpath.split(":", 1)
    path_to_data = path_to_datapack / f"data/{namespace}/{typification}/{relative_path}"
    for file in path_to_data.parent.iterdir():
        if file.is_file() and file.stem == path_to_data.name:
            return file
    raise FileNotFoundError(f"Can't find {path_to_data.name} in {path_to_data}")


def multi_replace(string: str, replacements: Sequence[Sequence[str]]) -> str:
    for old, new in replacements:
        string = string.replace(old, new)
    return string


def get_file_text(path: Path, encoding: str = None) -> str:
    """

    :param path: Path-object
    :param encoding: Encoding. Default value in config
    :return: File's content
    """
    with path.open(encoding=encoding) as f:
        return f.read()


def get_adv_json(path: Path, encoding: str = "utf-8") -> Optional[dict]:
    """

    :param path: Path-object
    :param encoding: Encoding. Default value in config
    :return: File's JSON
    """
    text = get_file_text(path, encoding)
    try:
        return json.loads(text)
    except json.decoder.JSONDecodeError:
        try:
            return json.loads(text.replace("\\'", ""))
        except json.decoder.JSONDecodeError:
            return None


def fill_pattern(text: str, values: dict[str, str]) -> str:
    pattern = r"\[<(\w+)>\]"

    def replace_pattern(match):
        key = match.group(1)
        return values.get(key, match.group(0))

    return re.sub(pattern, replace_pattern, text)


def get_with_multiple_values(input_dict: dict, *args: str | int, default: Any = None) -> Any | None:
    """
    Returns the value of the first key found in args within the input_dict.
    If none of the keys are found, return the default value.

    :param input_dict: Dictionary to search through.
    :param args: Keys to search for in the input_dict.
    :param default: Value to return if no keys are found in the dictionary.
    :return: The value corresponding to the first found key, or the default value if not found.
    """
    for key in args:
        if key in input_dict:
            return input_dict[key]
    return default


def arabic_to_rims(value: int) -> str:
    nums = {1000: "M", 900: "CM", 500: "D", 400: "CD", 100: "C", 90: "XC", 50: "L", 40: "XL", 10: "X", 9: "IX", 5: "V",
            4: "IV", 1: "I"}

    if value <= 0:
        raise ValueError("Value must be positive")

    result: str = ""
    for num in sorted(nums.keys(), reverse=True):
        while value >= num:
            result += nums[num]
            value -= num

    return result


def can_access_keypath(data: Dict[str, Any], keys: Iterable[str]) -> bool:
    """
    If it can get value by key-path, return True, else False
    :param data: Some dict.
    :param keys: List of keys.
    :return: True, if key-path in dict, else False
    """

    for key in keys:
        if isinstance(data, dict) and key in data:
            data = data[key]
        else:
            return False
    return True


def get_by_keypath(data: Dict[str, Any], keys: Iterable[str]) -> Optional[Any]:
    """
    If keys not in dict, will be return None
    :param data: Some dict.
    :param keys: List of keys to get value.
    :return: Value by keys.
    """

    for key in keys:
        if isinstance(data, dict) and key in data:
            data = data[key]
        else:
            return None
    return data


def merge_dicts(target: dict[str, Any], source: dict[str, Any]) -> None:
    """
    Merges `source` into `target`, similar to dict.update(), but with special handling for lists, sets, and tuples.

    If a key exists in both dictionaries:
      - If the values are lists, sets, or tuples, they are merged instead of being replaced.
      - Otherwise, the value from `source` replaces the value in `target`.

    :param target: The target dictionary to be updated.
    :param source: The source dictionary providing new values.
    """

    for key, value in source.items():
        if key in target:
            if isinstance(target[key], list) and isinstance(value, list):
                target[key].extend(value)
            elif isinstance(target[key], set) and isinstance(value, set):
                target[key].update(value)
            elif isinstance(target[key], tuple) and isinstance(value, tuple):
                target[key] += value
            elif isinstance(target[key], dict) and isinstance(value, dict):
                merge_dicts(target[key], value)
            else:
                target[key] = value
        else:
            target[key] = value
