from typing import Dict, Any

from .nbt_parser import nbt_decoder, nbt_encoder
from .utils import cut_namespace


def item_components_decoder(input_str: str) -> Dict[str, Any]:
    """
    Translate components to dict.
    :param input_str: Component.
    :return: Dict.
    """
    input_str = input_str[1:-1]
    result = {}
    current_key = ''
    current_value = ''
    in_key = True
    in_value = False
    brace_counter = 0
    signature = {"'": "'", "\"": "\"", "{": "}", "[": "]"}
    current_quote = None
    is_escaping = False
    i = 0

    while i < len(input_str):
        char = input_str[i]
        if in_key:
            if char == '=':
                current_key = cut_namespace(current_key)
                in_key = False
                in_value = True
            elif char not in [",", " "]:
                current_key += char
        elif in_value:
            if is_escaping:
                current_value += char
                is_escaping = False
            elif char == "\\":
                is_escaping = True
                current_value += char
            elif current_quote is None:
                if char == " ":
                    pass
                elif char == ",":
                    result[current_key.strip()] = current_value.strip()
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
                    result[current_key.strip()] = current_value.strip()
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
        result[current_key.strip()] = current_value.strip()

    result = {k: nbt_decoder(v) for k, v in result.items()}
    return result


def item_components_encoder(input_dict: Dict) -> str:
    """
    Translate dict to components.
    Also, it works dirtily, because text-json components in mc hardcoded.
    :param input_dict: Dict to translate.
    :return: Components.
    """

    #  add_quotes mean what components will be wrapped in ''
    #  If value is true, it's mean what each element of this one will be wrapped

    components = []
    for key, value in input_dict.items():
        value = nbt_encoder(value)
        components.append(f"{key}={value}")

    encoded_str = "[" + ", ".join(components) + "]"
    return encoded_str
