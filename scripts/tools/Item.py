import base64
import json
from io import BytesIO
from typing import Literal

import requests

from .Color import Color
from .utils import cut_namespace, get_with_multiple_values


class PlayerHead:
    def __init__(self, profile: dict[str, str | dict | list[dict]]) -> None:
        self._profile = profile
        if self._profile is not None:
            self._texture_url: str | None = \
            json.loads(base64.b64decode(self._profile["properties"][0]["value"]).decode())['textures']['SKIN']['url']
            self._head_hash_value: str | None = self._texture_url.rsplit('/', 1)[-1]
        else:
            self._texture_url = self._head_hash_value = None

        self._avatar: BytesIO | None = None
        self._avatar_size: int | None = 128
        self._avatar_direction: Literal["right", "left"] = "left"

    def fetch_avatar(self, size: int = 128, player_head_direction: Literal["right", "left"] = "left") -> BytesIO:
        """
        :param size: icon size from 32 to 600 px, default is 128
        :param player_head_direction: right or left
        :return: BytesIO data of avatar image
        """

        self.avatar_size = size
        self.avatar_direction = player_head_direction

        if self._head_hash_value is None:
            raise ValueError("Head hash value is None")

        response = requests.get(
            fr"https://mc-heads.net/head/{self._head_hash_value}/{self._avatar_size}/{self._avatar_direction}.png")

        if response.status_code == 200:
            self._avatar = BytesIO(response.content)
        else:
            response.raise_for_status()

        return self._avatar

    @property
    def avatar(self) -> BytesIO | None:
        """
        :return: Cached player head avatar, or None if it is not present
        """
        return self._avatar

    def get_or_fetch_avatar(self, size: int = 128, player_head_direction: Literal["right", "left"] = "left") -> BytesIO:
        """
        :param size: icon size from 32 to 600 px, default is 128
        :param player_head_direction: right or left
        :return:
        """

        if not self._avatar or size != self._avatar_size or self._avatar_direction != player_head_direction:
            self.fetch_avatar()
        return self._avatar

    @property
    def profile(self) -> dict | None:
        return self._profile

    @property
    def texture_url(self) -> str | None:
        return self._texture_url

    @property
    def head_hash_value(self) -> str:
        return self._head_hash_value

    @property
    def avatar_size(self) -> int | None:
        return self._avatar_size

    @property
    def avatar_direction(self) -> Literal["right", "left"]:
        return self._avatar_direction

    @avatar_direction.setter
    def avatar_direction(self, direction: Literal["right", "left"]) -> None:
        if direction not in ["right", "left"]:
            raise ValueError("direction must be either right or left")
        self._avatar_direction = direction

    @avatar_size.setter
    def avatar_size(self, size: int) -> None:
        if not 32 < size < 600:
            raise ValueError("Icon size must be between 32 and 600")
        self._avatar_size = size

    def __repr__(self):
        return f"PlayerHead(size:{self._avatar_size}, direction:{self._avatar_direction}, hash:{self._head_hash_value})"

    def __str__(self):
        return self.__repr__()


class Potion:
    def __init__(self, potion_contents: dict[str, str | int]) -> None:
        self._id = potion_contents["potion"]

        if potion_contents.get("custom_color", None):
            self._custom_color = Color(Color.int_to_hex(potion_contents["custom_color"]))
        else:
            self._custom_color = None

        self._custom_name = potion_contents.get("custom_name", None)

    @property
    def id(self) -> str:
        return self._id

    @property
    def custom_color(self) -> Color:
        """
        :return:
        """
        return self._custom_color

    @property
    def custom_name(self) -> str | None:
        return self._custom_name


class Item:
    def __init__(self, /, item_data: dict[str, str | dict | list] = None,
                 *, item_id: str = None, components: dict[str, str | dict | list] = None) -> None:
        if item_data is None and item_id is None:
            raise ValueError(
                "Either 'item_data' must be provided or both 'item_id' and 'components' must be specified.")

        if item_data:
            item_id = item_data["id"]
            components = item_data.get("components")
        self._id = item_id
        self._components = components
        if cut_namespace(item_id) == "player_head" and self.components is not None:
            profile = self._components.get("minecraft:profile") or self._components.get("profile")
            self._head_data = PlayerHead(profile)
        else:
            self._head_data = None

    @property
    def id(self) -> str:
        return self._id

    @property
    def components(self) -> dict | None:
        return self._components

    @property
    def enchantments(self) -> dict | None:
        return self.components.get("enchantments")

    @property
    def has_enchantment_glint(self) -> bool:
        enchantment_glint_override = get_with_multiple_values(self._components, "minecraft:enchantment_glint_override",
                                                              "enchantment_glint_override")
        if enchantment_glint_override is not None:
            return enchantment_glint_override
        else:
            return bool(self._components.get("enchantments", False))

    @property
    def is_head(self) -> bool:
        return self._head_data is not None

    @property
    def head_data(self) -> PlayerHead | None:
        return self._head_data

    def __repr__(self):
        return f"Item({self._id})"

    def __str__(self):
        return self.__repr__()


class RewardItem(Item):
    def __init__(self, item_id: str, components: dict[str, str | dict | list] | None,
                 item_type: Literal['item', 'block'], amount: str | int | None = 1) -> None:
        super().__init__(item_id=item_id, components=components)
        self._type = item_type
        self._amount = int(amount)

    @staticmethod
    def formatted_amount(amount: int) -> str:
        if amount <= 64:
            return str(amount)
        stacks = amount >> 6  # // 64
        remainder = amount & 63  # % 64
        remainder_str = f"+{remainder}" if remainder != 0 else ""
        return f"{stacks}x64{remainder_str}"

    @property
    def type(self) -> str:
        return self._type

    @property
    def amount(self) -> int:
        return self._amount

    def __repr__(self):
        return f"RewardItem(item:{self._id}, amount:{self._amount}, type:{self.type})"

    def __str__(self):
        return self.__repr__()


class TrophyItem(Item):
    def __init__(self, item_id: str, components: dict[str, str | dict | list], name: str, color: Color,
                 lore: str) -> None:
        super().__init__(item_id=item_id, components=components)
        self._name = name
        self._color = color
        self._lore = lore

    def regenerate_award_lore(self, adv_title: str, trophy_type_color: Color) -> None:
        """
        Regenerated trophy lore by data, parsed from a file.
        """
        self._components["lore"] = (self._components["lore"][:-3] +
                                    [{"text": " "},
                                     {"translate": "Awarded for achieving", "color": "gray"},
                                     {"translate": adv_title, "color": trophy_type_color.value, "italic": False}])

    @property
    def name(self) -> str:
        return self._name

    @property
    def color(self) -> Color:
        return self._color

    @property
    def lore(self) -> str:
        return self._lore

    def __repr__(self):
        return f"TrophyItem(item:{self._id}, name:{self._name})"

    def __str__(self):
        return self.__repr__()
