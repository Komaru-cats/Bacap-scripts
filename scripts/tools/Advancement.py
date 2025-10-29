import os
from collections import defaultdict
from functools import reduce

from . import Datapack
from .Criteria import CriteriaList
from .Functions import *
from .Item import *
from .Warnings import *
from .utils import *


class BaseAdvancement:
    """
    Base class for representing advancement in a datapack.
    This class is used as a base for other specific advancement classes like
    InvalidAdvancement, TechnicalAdvancement and Advancement.
    """

    def __init__(self, path: Path, datapack: Datapack, adv_json: dict, reward_mcpath: str = None, *args, **kwargs):
        """
        Initializes a new instance of the BaseAdvancement class.
        :param path: The file path to the advancement JSON file.
        :param datapack: The name of datapack.
        """
        self._adv_json = adv_json
        self._path = path
        self._datapack = datapack
        self._filename = path.stem
        self._namespace = str(path.relative_to(datapack.path / "data").parts[0])
        self._mc_path = path_to_mc_path(self.path)
        self._reward_mcpath = reward_mcpath

        if self._adv_json:
            self._parent = self._adv_json.get("parent")
        else:
            self._parent = None

        self._last_modified = os.path.getmtime(self._path)

    def delete(self) -> None:
        """
        Delete the current advancement
        :return: None
        """
        self._path.unlink()
        AdvancementsManager.remove(self)

    def create_reward_function(self):
        """
        Writes correct reward function inside JSON and updates an advancement file.
        """
        if not self._reward_mcpath:
            self._reward_mcpath = f"{self.datapack.reward_namespace}:{cut_namespace(self._mc_path)}"

        self._adv_json["rewards"] = {"function": self._reward_mcpath}
        self._path.write_text(json.dumps(self._adv_json, indent=2))

    @property
    def path(self) -> Path:
        """
        Returns the file path.
        """
        return self._path

    @path.setter
    def path(self, path: Path) -> None:
        """
        Change the advancement's path
        :param path: New path
        :return: None
        """
        self._path.unlink()
        self._path = path
        self._filename = path.stem
        self._mc_path = path_to_mc_path(path)
        self._reward_mcpath = f"{self.datapack.reward_namespace}:{cut_namespace(self._mc_path)}"
        self.json["rewards"]["function"] = self._reward_mcpath
        self._path.write_text(json.dumps(self.json, indent=2), encoding=self.datapack.encoding)

    @property
    def datapack(self) -> Datapack:
        """
        Returns the type of datapack.
        """
        return self._datapack

    @property
    def json_string(self) -> str:
        """
        Returns the content of the advancement JSON file as a string.
        """
        return self._path.read_text(encoding=self.datapack.encoding)

    def format_json(self) -> None:
        """
        Regenerated JSON with indents
        :return: None
        """
        self._path.write_text(json.dumps(self.json, indent=2))

    @property
    def json(self) -> dict | None:
        """
        Returns the JSON content of the advancement.
        """
        return self._adv_json

    @json.setter
    def json(self, new_json) -> None:
        self._adv_json = new_json

    @property
    def parent(self) -> str | None:
        """
        Returns the parent advancement, if any.
        """
        return self._parent

    @parent.setter
    def parent(self, parent: str):
        """
        Change the advancement's parent as mc_path
        :param parent: New parent path
        :return: None
        """
        self._parent = parent
        self.json["parent"] = parent
        self._path.write_text(json.dumps(self.json, indent=2), encoding=self.datapack.encoding)

    @property
    def mc_path(self) -> str:
        """
        Returns the path of the advancement in Minecraft format.
        """
        return self._mc_path

    @property
    def namespace(self) -> str:
        """
        Returns the namespace of the advancement.
        """
        return self._namespace

    @property
    def filename(self) -> str:
        """
        Returns the file name of the advancement without extension.
        """
        return self._filename

    @property
    def reward_mcpath(self) -> str:
        return self._reward_mcpath

    def __gt__(self, other):
        return self.mc_path > other.mc_path

    def __lt__(self, other):
        return self.mc_path < other.mc_path

    def __ge__(self, other):
        return self.mc_path >= other.mc_path

    def __le__(self, other):
        return self.mc_path <= other.mc_path

    @property
    def last_modified(self) -> float:
        """
        Property used for caching.
        Stores the last file modification time as a Unix timestamp.
        """
        return self._last_modified


class InvalidAdvancement(BaseAdvancement):
    """
    Class representing invalid advancement.
    Inherits from BaseAdvancement.
    """

    def __init__(self, path: Path, datapack: Datapack, adv_json, reason: AdvWarning, reward_mcpath: str = None):
        """
        Initializes a new instance of the InvalidAdvancement class.
        :param path: The file path to the advancement JSON file.
        :param datapack: The name of datapack.
        :param reason (str, optional): The reason why the advancement is considered invalid.
        """
        super().__init__(path, datapack, adv_json, reward_mcpath)
        self._reason = reason

    def __str__(self):
        return f"Invalid Advancement([{self.datapack}] {self._path})"

    def __repr__(self):
        return f"Invalid Advancement([{self.datapack}] {self._path})"

    @property
    def reason(self):
        """
        The reason why the advancement is considered invalid.
        """
        return self._reason


class TechnicalAdvancement(BaseAdvancement):
    """
    Class representing technical advancement.
    Inherits from BaseAdvancement.
    """

    def __init__(self, path: Path, datapack: Datapack, adv_json):
        """
        Initializes a new instance of the TechnicalAdvancement class.
        :param path: The file path to the advancement JSON file.
        :param datapack: The name of datapack.
        """
        super().__init__(path, datapack, adv_json)

    def __str__(self):
        return f"Technical Advancement([{self.datapack}] {self._path})"

    def __repr__(self):
        return f"Technical Advancement([{self.datapack}] {self._path})"


class Advancement(BaseAdvancement):
    """
    Class representing normal advancement.
    Inherits from BaseAdvancement.
    """
    tab_names = {"adventure": "Adventure", "animal": "Animals", "bacap": "B&C Advancements", "biomes": "Biomes",
                 "building": "Building",
                 "challenges": "Super Challenges", "enchanting": "Enchanting", "end": "The End", "farming": "Farming",
                 "mining": "Mining",
                 "monsters": "Monsters", "nether": "Nether", "potion": "Potions", "redstone": "Redstone",
                 "statistics": "Statistics", "weaponry": "Weaponry"}

    def __init__(self, path: Path, datapack: Datapack, adv_json: dict, reward_mcpath: str, tab: str, color: str,
                 frame: str, adv_type: str,
                 hidden: bool):
        """
        Creates a new instance of the Advancement class

        :param path: The file path to the advancement JSON file.
        :param datapack: The type of datapack.
        :param adv_json: The JSON data for the advancement.
        :param reward_mcpath: The path for the reward.
        :param tab: The tab for advancement.
        :param color: The color for the advancement.
        :param frame: The frame type for advancement.
        :param adv_type: The type of advancement.
        :param hidden: Whether the advancement is hidden.
        :return: An instance of Advancement.
        """

        super().__init__(path, datapack, adv_json, reward_mcpath)

        self._tab = tab
        self._color = Color(color)
        self._frame = frame
        self._hidden = hidden
        self._type = adv_type

        self._title = self._adv_json["display"]["title"]["translate"]
        self._description = self._adv_json["display"]["description"]["translate"]
        if "extra" in self._adv_json["display"]["description"]:
            self._get_description_from_extra()

        self._background = self._adv_json["display"].get("background")
        self._icon = Item(self._adv_json["display"]["icon"])
        self._criteria_list = CriteriaList(self._adv_json["criteria"])
        self._functions = Functions(self)

    def _get_description_from_extra(self):
        for item in self._adv_json["display"]["description"].get("extra", []):
            text_value = get_with_multiple_values(item, "text", "translate", default="")
            if isinstance(item, dict) and (
                    item.get("color") == self._color.value or text_value == "\n" or text_value.strip("\n") == ""):
                self._description += text_value
        self._description = self._description.rstrip("\n")

    def delete(self) -> None:
        """
        Delete the current advancement
        :return: None
        """
        self._path.unlink()
        self.functions.delete()
        AdvancementsManager.remove(self)

    def format_json(self) -> None:
        """
        Regenerated JSON with indents and set:
        reward-function, announce_to_chat
        :return: None
        """
        self._adv_json["display"]["announce_to_chat"] = True
        if not can_access_keypath(self.json, ("rewards", "function")) and self.datapack in DatapackList.work_with:
            self._adv_json["rewards"] = {"function": self.reward_mcpath}
        self._path.write_text(json.dumps(self.json, indent=2))

    @property
    def functions(self) -> Functions:
        """
        Returns the functions associated with the advancement.
        """
        return self._functions

    @property
    def title(self) -> str:
        """
        Returns the title of the advancement.
        """
        return self._title

    @title.setter
    def title(self, value: str) -> None:
        """
        Change the advancement's title in files
        :param value: New title of advancement
        :return: None
        """
        self.json["display"]["title"]["translate"] = value
        self._path.write_text(json.dumps(self.json, indent=2), encoding=self.datapack.encoding)
        self._title = value
        self.functions.msg.generate()
        self.functions.trophy.gen_from_selfdata()

    @property
    def description(self) -> str:
        """
        Returns the description of the advancement.
        """
        return self._description

    @description.setter
    def description(self, value: str) -> None:
        """
        Change the advancement's description in files
        :param value: New description of advancement
        :return: None
        """
        self.json["display"]["description"]["translate"] = value
        self._path.write_text(json.dumps(self.json, indent=2), encoding=self.datapack.encoding)
        self._description = value
        self.functions.msg.generate()

    @property
    def type(self) -> str:
        """
        Returns the technical type of the advancement (For bc_rewards, etc.).
        """
        if self._type == "advancement_legend":
            return "milestone"
        return self._type

    @type.setter
    def type(self, value: str) -> None:
        """
        Change the advancement's type in files
        :param value: New type of advancement
        :return: None
        """
        json_adv = self.json

        json_adv["display"]["description"]["color"] = self.datapack.adv_default_type_data[value]["color"]
        json_adv["display"]["frame"] = self.datapack.adv_default_type_data[value]["frame"]
        self._type = value

        self._path.write_text(json.dumps(json_adv, indent=2), encoding=self.datapack.encoding)
        self.functions.main.generate()
        self.functions.msg.generate()
        self.functions.trophy.gen_from_selfdata()

    @property
    def msg_type(self) -> str:
        """
        Returns the type of the advancement for message generation ONLY.
        """
        return self._type

    @property
    def tab_display(self):
        return self.tab_names.get(self._tab, "Undefined Tab")

    @BaseAdvancement.path.setter
    def path(self, path: Path) -> None:
        """
        Change the advancement's path
        :param path: New path
        :return: None
        """
        self._path.unlink()
        self._path = path
        self._filename = path.stem
        self._mc_path = path_to_mc_path(path)
        self._reward_mcpath = f"{self.datapack.reward_namespace}:{cut_namespace(self._mc_path)}"
        self.json["rewards"]["function"] = self._reward_mcpath
        self.functions.update_paths()
        self._tab = cut_namespace(self._reward_mcpath).split("/")[0]
        self._path.write_text(json.dumps(self.json, indent=2), encoding=self.datapack.encoding)

    @property
    def tab(self) -> str:
        """
        Returns the tab of the advancement.
        """
        return self._tab

    @property
    def color(self) -> Color | None:
        """
        Returns the color class of the advancement description.
        """
        return self._color

    @property
    def frame(self) -> str | None:
        """
        Returns the frame of the advancement.
        """
        return self._frame

    @property
    def hidden(self) -> bool:
        """
        Returns True if the advancement is hidden.
        """
        return self._hidden

    @hidden.setter
    def hidden(self, value: bool) -> None:
        if value:
            self._adv_json["display"]["description"]["color"] = self.datapack.default_hidden_color
        else:
            self._adv_json["display"]["description"]["color"] = self.datapack.adv_default_type_data[self._type]["color"]

        self._adv_json["display"]["hidden"] = value

        self._path.write_text(json.dumps(self._adv_json, indent=2), encoding=self.datapack.encoding)
        self.functions.main.generate()
        self.functions.msg.generate()
        self.functions.trophy.gen_from_selfdata()

    @property
    def background(self) -> str | None:
        """
        Returns a background path if it is root advancement.
        """
        return self._background

    @property
    def is_root(self) -> bool:
        """
        Returns true if the advancement is root, by checking the background path.
        """
        return self._background is not None

    @property
    def icon(self) -> Item:
        return self._icon

    @property
    def criteria_list(self) -> CriteriaList:
        """
        Returns a 'CriteriaList' of criteria for the advancement
        """
        return self._criteria_list


    def __str__(self):
        return f"Advancement([{self.datapack}] {self.mc_path})"

    def __repr__(self):
        return f"Advancement([{self.datapack}] {self.mc_path})"


class AdvancementFactory:
    @classmethod
    def load_advancement(cls, advancement_path: Path, datapack: Datapack,
                         force: bool = False) -> Advancement | InvalidAdvancement | TechnicalAdvancement:

        # Check, if advancement with this path already has been created,
        # return a cached object, else create and add to the cache
        if not force and advancement_path in AdvancementsManager and not cls._is_modified(advancement_path):
            return AdvancementsManager.adv_dict()[advancement_path]
        adv_json = get_adv_json(advancement_path)

        if cls._is_not_parsable_json(adv_json):
            return InvalidAdvancement(advancement_path, datapack, adv_json,
                                      AdvWarning(AdvWarningType.CANT_PARSE_JSON, "Invalid JSON"))

        if datapack.is_technical(advancement_path):
            return TechnicalAdvancement(advancement_path, datapack, adv_json)

        if cls._is_invalid_reward(adv_json):
            return InvalidAdvancement(advancement_path, datapack, adv_json,
                                      AdvWarning(AdvWarningType.REWARD_FUNCTION_DOESNT_SET,
                                                 "Can't get reward function"))

        reward_mcpath = adv_json["rewards"]["function"]

        if cls._is_invalid_translation(adv_json):
            return InvalidAdvancement(advancement_path, datapack, adv_json,
                                      AdvWarning(AdvWarningType.NO_TRANSLATE, "Can't get translation"), reward_mcpath)

        tab = cls._get_tab(reward_mcpath)

        color: str | None = adv_json["display"]["description"].get("color")
        frame: str | None = adv_json["display"].get("frame")
        hidden: bool = adv_json["display"].get("hidden", False)

        adv_type = datapack.resolve_adv_type(advancement_path.stem, tab, color, frame, hidden)

        if not adv_type:
            return InvalidAdvancement(advancement_path, datapack, adv_json,
                                      AdvWarning(AdvWarningType.UNKNOWN_TYPE, "Can't get type"), reward_mcpath)

        color = color or datapack.adv_default_type_data[adv_type]["color"]

        return Advancement(advancement_path, datapack, adv_json, reward_mcpath, tab, color, frame, adv_type, hidden)

    @classmethod
    def _is_modified(cls, advancement_path: Path) -> bool:
        return AdvancementsManager.adv_dict()[advancement_path].last_modified != os.path.getmtime(advancement_path)

    @staticmethod
    def _get_tab(reward_mcpath: str) -> str:
        return cut_namespace(reward_mcpath).split("/")[0]

    @staticmethod
    def _is_not_parsable_json(advancement_json: dict) -> bool:
        return advancement_json is None

    @staticmethod
    def _is_invalid_translation(advancement_json: dict) -> bool:
        required_keys = (
            ("display", "title", "translate"),
            ("display", "description", "translate")
        )
        return not all(can_access_keypath(advancement_json, keys) for keys in required_keys)

    @staticmethod
    def _is_invalid_reward(advancement_json: dict) -> bool:
        return not can_access_keypath(advancement_json, ("rewards", "function"))

    @classmethod
    def add_advancement(cls, path: Path, adv_json: dict, datapack: Datapack) -> None:
        """
        Function to save advancement.
        Also append it to Advancements.
        :param path: Path to the Advancement
        :param adv_json: JSON of the Advancement
        :param datapack: Datapack
        :return: None
        """
        path.write_text(json.dumps(adv_json, indent=2), encoding=datapack.encoding)
        adv = cls.load_advancement(path, datapack)
        if isinstance(adv, Advancement):
            adv.format_json()


class AdvManagerMeta(type):
    _advancements_list = None
    _advancements_dict = None

    def __getitem__(cls, key) -> InvalidAdvancement | TechnicalAdvancement | Advancement:
        if isinstance(key, int):
            return cls._advancements_dict[key]
        elif isinstance(key, Path):
            return cls._advancements_list.get(key)
        else:
            raise KeyError("Key must be an int (list index) or Path object")

    def __setitem__(cls, key, value) -> None:
        cls._advancements_dict[key] = value

    def __delitem__(cls, key) -> None:
        del cls._advancements_dict[key]

    def __contains__(self, item) -> bool:
        return item in self._advancements_dict


class AdvancementsManager(metaclass=AdvManagerMeta):
    """
    Methodical class for work with advancements.
    It automatically searches advancements and adds ones to the list.
    Contains advancement's list and iterator, append, remove and update methods
    """

    _advancements_dict: dict[Path, Advancement | InvalidAdvancement | TechnicalAdvancement] = {}
    _advancements_list: list[Advancement | InvalidAdvancement | TechnicalAdvancement] = []

    @classmethod
    def _generate_adv(cls):
        for datapack in DatapackList.available:
            for adv_paths in datapack.advancement_paths:
                for adv_path in adv_paths.rglob("*.json"):
                    if adv_path.is_file() and not datapack.is_excluded(adv_path):
                        cls._advancements_dict[adv_path] = AdvancementFactory.load_advancement(adv_path, datapack)
        cls._advancements_list = list(cls._advancements_dict.values())

    @classmethod
    def adv_list(cls) -> list[Advancement | InvalidAdvancement | TechnicalAdvancement]:
        return cls._advancements_list

    @classmethod
    def adv_dict(cls) -> dict[Path, Advancement | InvalidAdvancement | TechnicalAdvancement]:
        return cls._advancements_dict

    @classmethod
    def filtered_list(
            cls,
            datapack: Iterable[Datapack] | Datapack,
            skip_invalid: bool = True, skip_technical: bool = True, skip_normal: bool = False) -> list[
        Advancement | InvalidAdvancement | TechnicalAdvancement]:
        """
        Returns list of advancements by parameters.
        """
        return list(cls.filtered_iterator(datapack, skip_invalid, skip_technical, skip_normal))

    @staticmethod
    def __advancement_type_skip_check(adv: Advancement | InvalidAdvancement | TechnicalAdvancement, skip_invalid: bool,
                                      skip_technical: bool, skip_normal: bool):
        valid_advancement = not skip_invalid or not isinstance(adv, InvalidAdvancement)
        technical_advancement = not skip_technical or not isinstance(adv, TechnicalAdvancement)
        normal_advancement = not skip_normal or not isinstance(adv, Advancement)
        return valid_advancement and technical_advancement and normal_advancement

    @classmethod
    def filtered_iterator(
            cls,
            datapack: Iterable[Datapack] | Datapack,
            skip_invalid: bool = True,
            skip_technical: bool = True,
            skip_normal: bool = False
    ) -> Iterator[Advancement | InvalidAdvancement | TechnicalAdvancement]:
        """
        Return Iterator of advancements by parameters.
        """
        datapack = datapack if isinstance(datapack, Iterable) else (datapack,)
        for adv in cls._advancements_list:
            if datapack and (adv.datapack not in datapack):
                continue
            if cls.__advancement_type_skip_check(adv, skip_invalid, skip_technical, skip_normal):
                yield adv

    @classmethod
    def find(cls, criteria: dict[str, Any], datapack: Iterable[Datapack] | Datapack, limit: int = None,
             skip_invalid: bool = True, skip_technical: bool = True, skip_normal: bool = False,
             invert: bool = False) -> list[Advancement | InvalidAdvancement | TechnicalAdvancement]:
        """
        Returns list of advancements by search parameters.
        :param skip_normal: Skip normal Advancement if True.
        :param skip_technical: Skip technical Advancement if True.
        :param skip_invalid: Skip invalid Advancement if True.
        :param criteria: A dict, where key is attribute, value is expected value.
        :param datapack: The datapack.
        :param limit: How many find advancements. None if no limit
        :param invert: Invert find.
        If True, advancement, which fits the criteria, doesn't be added.
        :return: Instance of Advancement
        """
        iterator = cls.filtered_iterator(datapack, skip_invalid, skip_technical, skip_normal)
        advancement_list = []
        count = 0
        for adv in iterator:
            if limit and count >= limit:
                break
            for attr, value in criteria.items():
                if (getattr(adv, attr) == value) == invert:
                    continue
                count += 1
                advancement_list.append(adv)
        return advancement_list

    @classmethod
    def deep_find(cls, criteria: dict[str, Any], datapack: Iterable[Datapack] | Datapack, limit: int = None,
                  skip_invalid: bool = True, skip_technical: bool = True, skip_normal: bool = False,
                  invert: bool = False) -> list[Advancement | InvalidAdvancement | TechnicalAdvancement]:
        """
        Returns list of advancements by search parameters.
        :param skip_normal: Skip normal Advancement if True.
        :param skip_technical: Skip technical Advancement if True.
        :param skip_invalid: Skip invalid Advancement if True.
        :param criteria: A dict, where key is attribute, value is expected value.
        Key also can contain `.` and the value will be transformed to str.
        If value also can be callable and value didn't will be transformed
        :param datapack: The datapack.
        :param limit: How many find advancements. None if no limit
        :param invert: Invert find.
        If True, advancement, which fits the criteria, doesn't be added.
        :return: Instance of Advancement
        """

        def iterative_getattr(obj, attr):
            return reduce(getattr, attr.split('.'), obj)

        iterator = cls.filtered_iterator(datapack, skip_invalid, skip_technical, skip_normal)
        advancement_list = []
        count = 0
        for adv in iterator:
            if limit and count >= limit:
                break
            for criteria_attr, value in criteria.items():
                attr_value = iterative_getattr(adv, criteria_attr)

                if callable(value) and value(attr_value) == invert:
                    continue
                elif not callable(value):
                    value_in_attr = value in str(attr_value)
                    if value_in_attr == invert:
                        continue
                count += 1
                advancement_list.append(adv)
        return advancement_list

    @classmethod
    def remove(cls, adv: Advancement | InvalidAdvancement | TechnicalAdvancement | BaseAdvancement) -> None:
        """
        Remove advancement from Advancement's list.
        :param adv: Advancement to remove
        :return: None
        """
        cls._advancements_dict.pop(adv.path)

    @classmethod
    def generate(cls, force: bool = False) -> None:
        """
        Update All instances from files

        :param force: Clears the cache
        :return: None
        """
        if force:
            cls._advancements_dict.clear()
        cls._generate_adv()

    @classmethod
    def update_advancement(cls, path: Path, datapack: Datapack, force: bool = False) -> None:
        """
        Update only one advancement from a path
        :param datapack: Datapack class of the advancement
        :param path: Path class of the advancement
        :param force: Force Advancementlist to re-create the advancement and ignore caching (useful if you update only reward/trophy files)
        :return: None
        """
        cls._advancements_dict[path] = AdvancementFactory.load_advancement(path, datapack, force)
        cls._advancements_list = list(cls._advancements_dict.values())

    @classmethod
    def split_by_tabs(cls, advancements: Iterable[Advancement] = None) -> dict[str, list[Advancement]]:
        """
        Split advancements to tabs.
        :param advancements: Some Iterable type of Advancement.
        :return: Dict, where key is tab, value is a list of advancement in this tab.
        """
        if not advancements:
            advancements = cls._advancements_list
        folders = defaultdict(list)
        for adv in advancements:
            folders[adv.tab].append(adv)
        return folders
