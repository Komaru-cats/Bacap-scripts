import json
import re
from pathlib import Path
from typing import Dict, List

from .Color import Color
from .utils import mc_path_to_path

from collections.abc import Sequence


class Datapack:
    _instance = {}

    @staticmethod
    def generate_adv_parse_type_data(adv_type_data) -> Dict[str, Dict[str, re.Pattern]]:
        required_keys = {"filename", "tab", "color", "frame", "hidden"}

        for adv_type, criteria in adv_type_data.items():
            if set(criteria.keys()) != required_keys:
                raise KeyError(f"Invalid keys in adv_type_data for '{adv_type}'")

            for key in required_keys:
                criteria[key] = re.compile(criteria[key] + "$")

        return adv_type_data

    def __new__(cls, path_to_config_folder):
        if path_to_config_folder not in cls._instance:
            cls._instance[path_to_config_folder] = super().__new__(cls)
        return cls._instance[path_to_config_folder]

    def __init__(self, path_to_config_folder: Path):
        config = json.loads((path_to_config_folder / "settings.json").read_text(encoding="utf-8"))

        self._path = Path(config["path"])

        self._name = path_to_config_folder.name

        self._encoding = config.get('encoding', "utf-8")

        self._blacklisted_symbols = config.get("blacklisted_symbols", r"")
        self._language_pack = config.get("language_pack", None)

        if self._language_pack is not None:
            self._base_translation_path = Path(config["base_translation_path"]) \
                if config.get("base_translation_path", None) else None
            self._main_translation_path = Path(config["main_translation_path"])\
                if config.get("main_translation_path", None) else None

        base_translation_header_path = path_to_config_folder / "base_translation_header.txt"
        self._base_translation_header = (
            base_translation_header_path.read_text() if base_translation_header_path.exists() else None
        )
        self._start_floats_num = config.get("start_floats_num", 131)

        self._default_adv_namespace = config["default_adv_namespace"]
        self._adv_namespaces = config["adv_namespaces"]
        self._reward_namespace = config["reward_namespace"]
        self._fanpacks_namespace = config.get("fanpacks_namespace", "bacap_fanpacks")

        self._adv_parse_type_data = self.generate_adv_parse_type_data(config["adv_parse_type_data"])
        self._adv_default_type_data = config["adv_default_type_data"]

        self._legend_adv_mcpath = config.get('legend_adv_mcpath', None)

        self._milestone_adv_mcpaths = config.get("milestone_adv_mcpaths", {})
        self._empty_file = config.get("empty_file", '\n\n')

        self._generate_functions = config.get("generate_functions", False)

        self._install_mcpath = config.get("install_mcpath", None)

        release_name_pattern_path = path_to_config_folder / "release_name.pattern"
        self._release_name_pattern = release_name_pattern_path.read_text(
            encoding=self._encoding) if release_name_pattern_path.exists() else None

        install_mcfunc_pattern_path = path_to_config_folder / "install_mcfunc.pattern"
        self._install_mcfunc_pattern = install_mcfunc_pattern_path.read_text(
            encoding=self._encoding) if install_mcfunc_pattern_path.exists() else None

        self._tabs_have_branch = config.get("tabs_have_branch", None)

        self._override_hidden_msg = config.get("override_hidden_msg", False)

        self._default_hidden_color = config.get("default_hidden_data", {}).get("color", "light_purple")
        self._default_hidden_trophy_color = config.get("default_hidden_data", {}).get("trophy_color", "#FFAEFF")

        self._default_adv_namespace_path = self._path / f"data/{self._default_adv_namespace}"

        if self._legend_adv_mcpath:
            self._legend_adv_path = mc_path_to_path(self._path, "advancement", self._legend_adv_mcpath)
        else:
            self._legend_adv_path = None

        self._milestone_advs_path = {tab: mc_path_to_path(self._path, "advancement", adv) for tab, adv in
                                     self._milestone_adv_mcpaths.items()}

        self._adv_namespaces_paths = [self._path / f"data/{namespace}" for namespace in self._adv_namespaces]
        self._default_advancements_path = self._default_adv_namespace_path / "advancement"

        self._advancement_paths = [namespace_path / "advancement" for namespace_path in self._adv_namespaces_paths]

        self._function_path = self._path / f"data/{self._default_adv_namespace}/function"
        self._fanpacks_path = self._path / f"data/{self._fanpacks_namespace}"

        self._reward_namespace_path = self._path / f"data/{self._reward_namespace}"
        self._reward_path = self._reward_namespace_path / "function"

        if self._install_mcpath:
            self._install_path = mc_path_to_path(self._path, "function", self._install_mcpath)
        else:
            self._install_path = None

        self._technical_paths = [self.default_advancements_path / tech_folder for tech_folder in
                                 config["technical_paths"]]
        self._excluded_paths = [self.default_advancements_path / excluded_folder for excluded_folder in
                                config["excluded_paths"]]

        if config.get("use_default_msg", True):
            self._msg_patterns_path = (path_to_config_folder.parent / "default_msg").resolve()
        else:
            self._msg_patterns_path = path_to_config_folder / "msg"

        self._msg_patterns = {pattern.stem: pattern.read_text(encoding=self._encoding) for pattern in
                              self._msg_patterns_path.iterdir() if pattern.suffix == ".pattern"}
        self._msg_milestone_names = json.loads(
            (self._msg_patterns_path / "milestone_names.json").read_text(encoding=self._encoding))

    def is_technical(self, path):
        return any(path.is_relative_to(tech_folder) for tech_folder in self.technical_paths)

    def is_excluded(self, path):
        return any(path.is_relative_to(excl_folder) for excl_folder in self.excluded_paths)

    def resolve_adv_type(self,
                         filename: str | None = None,
                         tab: str | None = None,
                         color: str | None = None,
                         frame: str | None = None,
                         hidden: bool | str = False):
        matches = []
        for key, criteria in self.adv_parse_type_data.items():
            if ((filename is None or re.match(criteria['filename'], filename)) and
                    (tab is None or re.match(criteria['tab'], tab)) and
                    (color is None or re.match(criteria['color'], color)) and
                    (frame is None or re.match(criteria['frame'], frame)) and
                    (hidden is None or re.match(criteria['hidden'], str(hidden)))):
                matches.append(key)
        if not matches:
            return None
        return matches[0]

    def __repr__(self):
        return self.name

    @property
    def path(self) -> Path:
        return self._path

    @property
    def name(self) -> str:
        return self._name

    @property
    def encoding(self) -> str:
        return self._encoding

    @property
    def language_pack(self) -> str:
        return self._language_pack

    @property
    def base_translation_path(self) -> Path:
        return self._base_translation_path

    @property
    def start_floats_num(self) -> int:
        return self._start_floats_num

    @property
    def main_translation_path(self) -> Path:
        return self._main_translation_path

    @property
    def base_translation_header(self) -> str | None:
        return self._base_translation_header

    @property
    def default_adv_namespace(self) -> str:
        return self._default_adv_namespace

    @property
    def adv_namespaces(self) -> List[str]:
        return self._adv_namespaces

    @property
    def fanpacks_namespace(self) -> str:
        return self._fanpacks_namespace

    @property
    def tabs_have_branch(self) -> List[str]:
        return self._tabs_have_branch

    @property
    def excluded_paths(self) -> List[Path]:
        return self._excluded_paths

    @property
    def empty_file(self) -> str:
        return self._empty_file

    @property
    def generate_functions(self) -> bool:
        return self._generate_functions

    @property
    def default_hidden_color(self) -> None | str:
        return self._default_hidden_color

    @property
    def override_hidden_msg(self) -> bool:
        return self._override_hidden_msg

    @property
    def release_name_pattern(self) -> str:
        return self._release_name_pattern

    @property
    def install_mcfunc_pattern(self) -> str:
        return self._install_mcfunc_pattern

    @property
    def install_mcpath(self) -> str:
        return self._install_mcpath

    @property
    def legend_adv_mcpath(self) -> str:
        return self._legend_adv_mcpath

    @property
    def milestone_adv_mcpaths(self) -> Dict[str, str]:
        return self._milestone_adv_mcpaths

    @property
    def reward_namespace(self) -> str:
        return self._reward_namespace

    @property
    def msg_patterns(self) -> Dict[str, str]:
        return self._msg_patterns

    @property
    def msg_milestone_names(self) -> Dict[str, Dict[str, str]]:
        return self._msg_milestone_names

    @property
    def default_adv_namespace_path(self) -> Path:
        return self._default_adv_namespace_path

    @property
    def adv_namespaces_paths(self):
        return self._adv_namespaces_paths

    @property
    def default_advancements_path(self) -> Path:
        return self._default_advancements_path

    @property
    def advancement_paths(self) -> List[Path]:
        return self._advancement_paths

    @property
    def reward_namespace_path(self) -> Path:
        return self._reward_namespace_path

    @property
    def reward_path(self) -> Path:
        return self._reward_path

    @property
    def function_path(self) -> Path:
        return self._function_path

    @property
    def fanpacks_path(self) -> Path:
        return self._fanpacks_path

    @property
    def msg_patterns_path(self) -> Path:
        return self._msg_patterns_path

    @property
    def install_path(self) -> Path:
        return self._install_path

    @property
    def legend_adv_path(self) -> Path:
        return self._legend_adv_path

    @property
    def milestone_advs_path(self) -> Dict[str, Path]:
        return self._milestone_advs_path

    @property
    def technical_paths(self) -> Sequence[Path]:
        return self._technical_paths

    @property
    def adv_parse_type_data(self) -> Dict[str, Dict[str, re.Pattern]]:
        return self._adv_parse_type_data

    @property
    def adv_default_type_data(self) -> Dict[str, Dict[str, str]]:
        return self._adv_default_type_data

    @property
    def blacklisted_symbols(self) -> str:
        return self._blacklisted_symbols

    def get_trophy_text_color_by_type(self, adv_type: str, is_hidden: bool = False):
        if is_hidden:
            return Color(self._default_hidden_trophy_color)
        return Color(self._adv_default_type_data[adv_type]['trophy_color'])

    def __eq__(self, other: "Datapack") -> bool:
        return self.name == other.name and self.path == other.path

    def is_bacap(self) -> bool:
        return self == DatapackList.bacap


class DatapackList:
    datapack_list_json = json.loads(Path("config/datapacklist.json").read_text())
    available: List[Datapack] = [Datapack(Path(f"config/{datapack}")) for datapack in datapack_list_json["available"]]
    work_with: List[Datapack] = [Datapack(Path(f"config/{datapack}")) for datapack in datapack_list_json["work_with"]]
    default: Datapack = Datapack(Path(f"config/{datapack_list_json["default"]}"))
    bacap: Datapack = Datapack(Path(f"config/{datapack_list_json["bacap"]}"))
