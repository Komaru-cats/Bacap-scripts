import json
from pathlib import Path
from typing import Dict, List


class ItemProperties:
    dict: Dict[str, Dict[str, str | int]] = json.loads(Path("resources/items.json").read_text())
    list: List[str] = list(dict.keys())
    names_list = [item['display_name'].lower() for item in dict.values()]


class BlockProperties:
    dict: Dict[str, Dict[str, str | int]] = json.loads(Path("resources/blocks.json").read_text())
    list: List[str] = list(dict.keys())
    names_list = [block['display_name'].lower() for block in dict.values()]


class DyeColors:
    dict: Dict[str, int] = json.loads(Path("resources/dye_colors.json").read_text())
    list: List[str] = list(dict.keys())


class Containers:
    list: List[str] = json.loads(Path("resources/containers.json").read_text())


class Effects:
    list: List[str] = json.loads(Path("resources/effects.json").read_text())


class Enchantments:
    dict: Dict[str, int] = json.loads(Path("resources/enchantments.json").read_text())
    list: List[str] = list(dict.keys())
    curses: List[str] = {"binding_curse", "vanishing_curse"}


class FireworkShapes:
    list: List[str] = json.loads(Path("resources/firework_shapes.json").read_text())


class BannerPatterns:
    list: List[str] = json.loads(Path("resources/banner_patterns.json").read_text())


class TrimList:
    list: List[str] = json.loads(Path("resources/trim_list.json").read_text())


class Potion:
    dict: Dict[str, Dict[str, bool]] = json.loads(Path("resources/potion.json").read_text())
    list: List[str] = dict.keys()


class TrimMaterialColor:
    dict: Dict[str, str] = json.loads(Path("resources/trim_material_color.json").read_text())
    list: List[str] = dict.keys()


class TextColors:
    dict: Dict[str, str] = json.loads(Path("resources/text_colors.json").read_text())
    reverse_dict: Dict[str, str] = {v: k for k, v in dict.items()}
    list: List[str] = dict.keys()
