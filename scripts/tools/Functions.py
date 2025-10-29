from . import Advancement, DatapackList
from .Color import Color
from .Item import TrophyItem, RewardItem
from .Patterns import FunctionsWritePatterns, FunctionsReadPatterns
from .Resources import ItemProperties
from .components_parser import item_components_decoder, item_components_encoder
from .nbt_parser import nbt_decoder, nbt_encoder
from .utils import *


class FuncMixin:
    """
    Mixin for rewards
    """

    _mc_path_not_empty = set()

    def __init__(self, advancement: Advancement, path: Path, mc_path: str):
        self._adv = advancement
        self._path = path
        self._mc_path = mc_path
        self._exist = None
        self._empty_generated = None
        self._empty = None

    @property
    def path(self):
        return self._path

    @property
    def mc_path(self):
        return self._mc_path

    @property
    def mc_path_empty(self):
        self.create_file_state()
        return self._mc_path not in self._mc_path_not_empty

    @property
    def exist(self):
        self.create_file_state()
        return self._exist

    @property
    def empty(self):
        self.create_file_state()
        return self._empty

    @property
    def empty_generated(self):
        self.create_file_state()
        return self._empty_generated

    def create_file_state(self):
        if self._path.exists():
            self._exist = True
            content = self._path.read_text(encoding=self._adv.datapack.encoding)
            self._empty_generated = content == self._adv.datapack.empty_file
            self._empty = content == ""
        else:
            self._empty = True
            self._empty_generated = False
            self._exist = False
        if not self._empty:
            self._mc_path_not_empty.add(self._mc_path)

    @property
    def content(self) -> str:
        if self._path.exists():
            content = self._path.read_text(encoding=self._adv.datapack.encoding)
            return content
        else:
            return ""

    @content.setter
    def content(self, new_content: str) -> None:
        if self._path.exists():
            self._path.write_text(new_content, encoding=self._adv.datapack.encoding)
        else:
            raise FileNotFoundError("Can't write to file", self._path)

    def _write_file(self, content):
        if not self._path.parent.exists():
            self._path.parent.mkdir(parents=True, exist_ok=True)
        self._path.write_text(content, encoding=self._adv.datapack.encoding)


class Main(FuncMixin):
    """
    Class for main's file to run functions.
    """

    def __init__(self, advancement: Advancement, path: Path, mc_path: str):
        super().__init__(advancement, path, mc_path)

    def generate(self) -> None:
        """
        Generate main's file.
        :adv_type: type of the advancements
        :adv_mc_path: minecraft_path of the advancement
        :return: None
        """
        if not self._adv.datapack.generate_functions:
            return
        reward_path = cut_namespace(self.mc_path)
        self._write_file(fill_pattern(FunctionsWritePatterns.main,
                                      {"type": self._adv.type, "adv_path": self._adv.mc_path,
                                       "adv_score_disabler": "#" if self._adv.hidden else "",
                                       "reward_namespace": self._adv.datapack.reward_namespace,
                                       "reward_path": reward_path,
                                       "fanpacks_namespace": self._adv.datapack.fanpacks_namespace,
                                       "bacap_reward_namespace": DatapackList.bacap.reward_namespace}))


class Exp(FuncMixin):
    """
    Class for exp's reward.
    """

    def __init__(self, advancement: Advancement, path: Path, mc_path: str):
        super().__init__(advancement, path, mc_path)
        self._exp = None
        self.__parse_from_file()

    def __parse_from_file(self):
        search = re.search(FunctionsReadPatterns.exp_command, self.content)
        if search:
            self._exp = int(search.groups()[0])
        else:
            self._exp = None

    def generate(self, exp: Union[str, int, None]) -> None:
        """
        Generate exp's file.
        :param exp: Amount of experience.
        :return: None
        """
        if not self._adv.datapack.generate_functions:
            return
        if exp:
            self._exp = int(exp)
            self._write_file(fill_pattern(FunctionsWritePatterns.exp, {"exp": str(self._exp)}))
        else:
            self._write_file(self._adv.datapack.empty_file)

    @property
    def value(self) -> Optional[int]:
        """
        Returns amount of exp or None, if it doesn't set
        """
        return self._exp


class Msg(FuncMixin):
    """
    Class for msg's function.
    """

    def __init__(self, advancement: Advancement, path: Path, mc_path: str):
        super().__init__(advancement, path, mc_path)

    def generate(self) -> None:
        """
        Generate msg's file.
        :is_hidden_adv: Hidden adv or not
        :return: None
        """
        if not self._adv.datapack.generate_functions:
            return

        if self._adv.datapack.override_hidden_msg and self._adv.hidden:
            msg_type = "hidden"
        else:
            msg_type = self._adv.msg_type

        name = self._adv.title.replace('"', r'\"')
        desc = self._adv.description.replace('"', r'\"').replace('\n', r'\n')

        if msg_type == "milestone":
            for key, value in self._adv.datapack.msg_milestone_names.items():
                if value['milestone'] == self._adv.title.title:
                    tab = value["name"]
                    break
            else:
                return
        else:
            tab = self._adv.datapack.msg_milestone_names[self._adv.tab]["name"]

        self._write_file(
            fill_pattern(self._adv.datapack.msg_patterns[msg_type], {"desc": desc, "name": name, "tab": tab}))


class Reward(FuncMixin):
    """
    Class for reward's functions.
    """

    def __init__(self, advancement: Advancement, path: Path, mc_path: str):
        super().__init__(advancement, path, mc_path)
        self._item = None
        self._command_type = None
        self.__parse_from_file()

    def __parse_from_file(self):
        content = self.content

        item_type_match = re.search(r"tellraw .*?{\"translate\":\"(item|block)", content)
        item_type = item_type_match.group(1) if item_type_match else None

        match = re.search(FunctionsReadPatterns.give_command, content)
        if match:
            command_data = match.groupdict()
            self._command_type = "give"

            components = item_components_decoder(command_data["components"]) if command_data.get("components") else None
            self._item = RewardItem(command_data["item_id"], components, item_type, command_data["amount"])
            return

        match = re.search(FunctionsReadPatterns.summon_command, content)
        if match:
            nbt_data = nbt_decoder(match.groupdict()["nbt"])
            self._command_type = "summon"

            self._item = RewardItem(nbt_data["Item"]["id"], nbt_data["Item"]["count"], item_type,
                                    nbt_data["Item"].get("components"))

    def generate(self, item_id: str | None, amount: str | int | None = "1",
                 command: Literal["give", "summon"] = "give", components: Dict[str, Any] = None) -> str | None:
        """
        :param item_id: The id of item.
        If item_id is None, generate an empty file.
        :param amount: The number of rewards.
        :param command: Command type (summon or give).
        :param components: Another data in item's components.
        :return:
        """
        if not item_id:
            self._write_file(self._adv.datapack.empty_file)
            self._item = None
            self._command_type = None
            self.__parse_from_file()
            return None

        if components and "stored_enchantments" in components.keys():
            enchantments: dict[str, str] = components["stored_enchantments"]
            enchantment_book = "enchantment.minecraft." + cut_namespace(list(enchantments.keys())[0])
            enchantment_level = arabic_to_rims(int(list(enchantments.values())[0]))
            enchantment_name = fill_pattern(FunctionsWritePatterns.enchantment_msg,
                                            {"id": enchantment_book, "level": enchantment_level})
        else:
            enchantment_name = ""
        formated_amount = RewardItem.formatted_amount(amount)
        replace_dict = {"formated_amount": formated_amount, "type": ItemProperties.dict[item_id]["type"],
                        "enchantment_name": enchantment_name, "item_id": item_id}
        tellraw = fill_pattern(FunctionsWritePatterns.reward_msg, replace_dict)
        item_id = cut_namespace(item_id)
        if command == "give":
            components = item_components_encoder(components) if components else ""
            give_command = f"give @s {item_id}{components} {amount}\n"
        else:
            nbt = {"Invulnerable": True,
                   "Item":
                       {
                           "id": item_id,
                           "count": amount,
                           "components": components
                       }
                   }
            give_command = ""
            while amount > 0:
                nbt["Item"]["count"] = min(amount, 64)
                give_command += f"summon minecraft:item ~ ~ ~ {nbt_encoder(nbt)}\n"
                amount -= 64
        summon_tellraw = "The reward appeared at the place of your death" if command == "summon" else ""
        self._write_file(give_command + tellraw)
        self.__parse_from_file()
        return give_command + tellraw + summon_tellraw

    @property
    def item(self) -> RewardItem:
        """
        Return item's.
        """
        return self._item

    @property
    def command_type(self):
        """
        Return command's name ("give" or "summon")
        """
        return self._command_type


class Trophy(FuncMixin):
    item_id_counter = Counter()

    def __init__(self, advancement: Advancement, path: Path, mc_path: str):
        super().__init__(advancement, path, mc_path)
        self._command_type = None
        self._item = None
        self.__parse_from_file()

    @staticmethod
    def __parse_description(lore: List) -> List:
        desc_list = []
        lore = lore[:-3]
        for line in lore:
            if isinstance(line, dict):
                desc_list.append(get_with_multiple_values(line, "text", "translate"))
            elif isinstance(line, list):
                desc_list.append("".join([get_with_multiple_values(element, "text", "translate") for element in line]))
        return desc_list

    def __parse_from_file(self) -> None:
        give_pattern = FunctionsReadPatterns.give_command_trophy
        summon_pattern = FunctionsReadPatterns.summon_command_trophy

        give_search = re.search(give_pattern, self.content)
        if give_search:
            self._command_type = "give"
            item_id = give_search["item_id"]
            components = item_components_decoder(give_search.groupdict()["components"])
        else:
            summon_search = re.search(summon_pattern, self.content)
            if not summon_search:
                return  # Ни одна команда не найдена, выходим

            self._command_type = "summon"
            nbt = nbt_decoder(summon_search.groupdict()["nbt"])
            item_id = nbt["Item"]["id"]
            components = nbt["Item"]["components"]

        custom_name = get_with_multiple_values(components, "custom_name", "item_name")
        name = get_with_multiple_values(custom_name, "text", "translate")
        color = custom_name.get("color", None)

        if color:
            color = Color(color)

        lore = "\n".join(x for x in self.__parse_description(components.get("lore", [])) if ".minecraft." not in x)

        self._item = TrophyItem(item_id=item_id, components=components, name=name, color=color, lore=lore)

    def generate(self, item_id: str | None, name: str = None, description: Iterable[str] = None, color: str = None,
                 command: Literal["give", "summon"] = "give", components: Dict[str, Any] = None) -> Optional[str]:
        """
        Generate a trophy's file with args.
        :param item_id: The id of item.
        If item_id is None, generate an empty file
        :param name: The name of trophy.
        :param description: The description below the item's name.
        :param color: Color of a trophy's text.
        :param command: Command type (summon or give).
        :param components: Another data in item's components
        """

        if item_id is None:
            self._write_file(self._adv.datapack.empty_file)
            self._command_type = None
            self._item = None
            self.__parse_from_file()
            return None

        elif not (name and description and color):
            raise ValueError("'name' and/or 'description' and/or 'color' doesn't set")
        if not components:
            components = {}
        if "lore" not in components.keys():
            components["lore"] = []

        lore = [{"translate": part, "color": color} for part in description]
        components["lore"] = lore + components["lore"] + [{"text": " "},
                                                          {"translate": "Awarded for achieving", "color": "gray"},
                                                          {"translate": self._adv.title,
                                                           "color": self._adv.datapack.get_trophy_text_color_by_type(
                                                               self._adv.type, self._adv.hidden), "italic": False}]
        self.item_id_counter[item_id] += 1

        components.update({
            "custom_name": {
                "translate": name,
                "color": color,
                "bold": True,
                "italic": False
            },
            "custom_model_data": {"floats": [self.item_id_counter[item_id] + self._adv.datapack.start_floats_num]},
            "custom_data": {"Trophy": 1},
        })

        tellraw_msg = {"color": "gold", "text": " +1 ", "extra": [{"translate": name}]}
        if command == "give":
            text_command = (f"give @s {item_id}{item_components_encoder(components)} 1\n"
                            f"tellraw @s {json.dumps(tellraw_msg, ensure_ascii=False)}")

        elif command == "summon":
            tellraw_msg_summon = {"color": "gray", "translate": " The trophy appeared at the place of your death"}
            nbt = {"Invulnerable": True,
                   "Item":
                       {
                           "id": item_id,
                           "count": 1,
                           "components": components
                       }
                   }
            text_command = (f"summon minecraft:item ~ ~ ~ {nbt_encoder(nbt)}\n"
                            f"tellraw @s {json.dumps(tellraw_msg, ensure_ascii=False)}\n"
                            f"tellraw @s {json.dumps(tellraw_msg_summon, ensure_ascii=False)}")
        else:
            raise ValueError("Command may be only 'summon' or 'give'")

        self._write_file(text_command)
        self.__parse_from_file()
        return text_command

    def gen_from_selfdata(self):
        """
        Regenerated trophy by data, parsed from a file.
        :return:
        """
        if not self._adv.datapack.generate_functions:
            return

        if self.empty:
            self._write_file("")
            return ""

        elif self.empty_generated:
            self._write_file(self._adv.datapack.empty_file)
            return self._adv.datapack.empty_file

        self._item.regenerate_award_lore(self._adv.title,
                                         self._adv.datapack.get_trophy_text_color_by_type(self._adv.type,
                                                                                          self._adv.hidden))

        tellraw_msg = {"color": "gold", "text": " +1 ", "extra": [{"translate": self.item.name}]}

        components = self._item.components
        components.update({
            "custom_model_data": {"floats": [self.item_id_counter[self.item.id] + self._adv.datapack.start_floats_num]},
        })

        if cut_namespace(self.item.id) != "player_head":
            self.item_id_counter[cut_namespace(self.item.id)] += 1

        if self.command_type == "give":
            file_content = (f"give @s {self.item.id}{item_components_encoder(components)} 1\n"
                            f"tellraw @s {json.dumps(tellraw_msg, ensure_ascii=False)}")

        elif self.command_type == "summon":
            tellraw_msg_summon = {"color": "gray", "text": " The trophy appeared at the place of your death"}

            nbt = {"Invulnerable": True,
                   "Item":
                       {
                           "id": self.item.id,
                           "count": 1,
                           "components": components
                       }
                   }

            file_content = (f"summon minecraft:item ~ ~ ~ {nbt_encoder(nbt)}\n"
                            f"tellraw @s {json.dumps(tellraw_msg, ensure_ascii=False)}\n"
                            f"tellraw @s {json.dumps(tellraw_msg_summon, ensure_ascii=False)}")

        else:
            raise ValueError("Command may be only 'summon' or 'give'")

        self._write_file(file_content)
        self.__parse_from_file()
        return file_content

    @property
    def item(self) -> TrophyItem:
        """
        Return trophy's item's class.
        """
        return self._item

    @property
    def command_type(self) -> Optional[str]:
        """
        Return trophy's command's name ("give" or "summon").
        """
        return self._command_type


class Functions:
    """
    Class to work with advancement's rewards
    """
    exist_mc_path = set()

    def __init__(self, adv: "Advancement"):
        self._adv = adv
        self._main = None
        self._exp = None
        self._msg = None
        self._reward = None
        self._trophy = None
        path_to_reward = cut_namespace(self._adv.reward_mcpath)
        self.main_path = adv.datapack.reward_path / (path_to_reward + ".mcfunction")
        self.exp_path = adv.datapack.reward_path / ("exp/" + path_to_reward + ".mcfunction")
        self.msg_path = adv.datapack.reward_path / ("msg/" + path_to_reward + ".mcfunction")
        self.reward_path = adv.datapack.reward_path / ("reward/" + path_to_reward + ".mcfunction")
        self.trophy_path = adv.datapack.reward_path / ("trophy/" + path_to_reward + ".mcfunction")

        self.mc_main_path = path_to_mc_path(self.main_path)
        self.mc_exp_path = path_to_mc_path(self.exp_path)
        self.mc_msg_path = path_to_mc_path(self.msg_path)
        self.mc_reward_path = path_to_mc_path(self.reward_path)
        self.mc_trophy_path = path_to_mc_path(self.trophy_path)
        self._expand_exist_mc_paths()

    def _expand_exist_mc_paths(self):
        paths = [
            (self.main_path, self.mc_main_path),
            (self.exp_path, self.mc_exp_path),
            (self.msg_path, self.mc_msg_path),
            (self.reward_path, self.mc_reward_path),
            (self.trophy_path, self.mc_trophy_path)
        ]
        for path, mc_path in paths:
            if path.exists():
                self.exist_mc_path.add(mc_path)

    def _reset_cache(self):
        self._main = None
        self._exp = None
        self._msg = None
        self._reward = None
        self._trophy = None

    def update_paths(self) -> None:
        """
        Update functions file's by updating advancement's params.
        :return: None
        """
        path_to_reward = cut_namespace(self._adv.reward_mcpath)
        new_main_path = self._adv.datapack.reward_path / (path_to_reward + ".mcfunction")
        new_exp_path = self._adv.datapack.reward_path / ("exp/" + path_to_reward + ".mcfunction")
        new_msg_path = self._adv.datapack.reward_path / ("msg/" + path_to_reward + ".mcfunction")
        new_reward_path = self._adv.datapack.reward_path / ("reward/" + path_to_reward + ".mcfunction")
        new_trophy_path = self._adv.datapack.reward_path / ("trophy/" + path_to_reward + ".mcfunction")
        if self.main_path.exists():
            self.main_path.rename(new_main_path)
        if self.exp_path.exists():
            self.exp_path.rename(new_exp_path)
        if self.msg_path.exists():
            self.msg_path.rename(new_msg_path)
        if self.reward_path.exists():
            self.reward_path.rename(new_reward_path)
        if self.trophy_path.exists():
            self.trophy_path.rename(new_trophy_path)
        self.main_path = new_main_path
        self.exp_path = new_exp_path
        self.msg_path = new_msg_path
        self.reward_path = new_reward_path
        self.trophy_path = new_trophy_path
        self._reset_cache()

    def delete(self) -> None:
        """
        Delete all reward files.
        :return: None
        """
        self.main_path.unlink(missing_ok=True)
        self.exp_path.unlink(missing_ok=True)
        self.msg_path.unlink(missing_ok=True)
        self.reward_path.unlink(missing_ok=True)
        self.trophy_path.unlink(missing_ok=True)
        self._reset_cache()

    def get_non_existent_files(self) -> Tuple[str, ...]:
        """
        Return Generator of function files, which doesn't exist.
        :return: Generator with str.
        """
        exist_dict = {
            "main": self.mc_main_path in self.exist_mc_path,
            "exp": self.mc_exp_path in self.exist_mc_path,
            "msg": self.mc_msg_path in self.exist_mc_path,
            "reward": self.mc_reward_path in self.exist_mc_path,
            "trophy": self.mc_trophy_path in self.exist_mc_path,
        }
        doesnt_exist = tuple(k for k, v in exist_dict.items() if not v)
        return doesnt_exist

    def get_empty_files(self) -> Tuple[str, ...]:
        """
        Return list of function files, which is full empty.
        Files with empty lines ignored because, empty line meaning what reward it None.
        :return: Tuple with str.
        """
        empty_dict = {
            "main": self.main.mc_path_empty,
            "exp": self.exp.mc_path_empty,
            "msg": self.msg.mc_path_empty,
            "reward": self.reward.mc_path_empty,
            "trophy": self.trophy.mc_path_empty,
        }
        empty = tuple(k for k, v in empty_dict.items() if v)
        return empty

    @property
    def main(self) -> Main:
        """
        Instance of main's file.
        This file is used to call all functions rewards correctly.
        Contains generate function.
        """
        if self._main is None:
            self._main = Main(self._adv, self.main_path, self.mc_main_path)
        return self._main

    @property
    def exp(self) -> Exp:
        """
        Instance of exp's file.
        This file is used to get exp.
        Contains generate function, parser, and property of exp amount.
        """
        if self._exp is None:
            self._exp = Exp(self._adv, self.exp_path, self.mc_exp_path)
        return self._exp

    @property
    def msg(self) -> Msg:
        """
        Instance of msg's file.
        This file is used to send msg in mc chat.
        Contains generate function.
        """
        if self._msg is None:
            self._msg = Msg(self._adv, self.msg_path, self.mc_msg_path)
        return self._msg

    @property
    def reward(self) -> Reward:
        """
        Instance of reward's file.
        This file is used to get items to player as reward.
        Contains generate function, parser, and reward properties.
        """
        if self._reward is None:
            self._reward = Reward(self._adv, self.reward_path, self.mc_reward_path)
        return self._reward

    @property
    def trophy(self) -> Trophy:
        """
        Instance of trophy's file.
        This file is used to get trophy.
        Contains generate function, parser, and trophy properties.
        """
        if self._trophy is None:
            self._trophy = Trophy(self._adv, self.trophy_path, self.mc_trophy_path)
        return self._trophy
