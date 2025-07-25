from .Resources import TextColors


class Color:
    def __init__(self, color: str):
        self._color = color

    @property
    def value(self):
        return self._color

    @value.setter
    def value(self, color: str):
        self._color = color

    @property
    def as_hex(self):
        if self._color[0] == "#":
            return self._color
        else:
            try:
                return TextColors.dict[self._color]
            except KeyError:
                raise ValueError(f"'{self._color}' is not a valid color")

    @property
    def as_rgb(self):
        hex_color = self.as_hex.removeprefix("#")
        return int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)

    @property
    def as_int(self):
        return int(self.as_hex.removeprefix("#"), 16)

    def __repr__(self):
        return self._color

    @classmethod
    def color_to_hex(cls, color: str) -> str:
        if color[0] == "#":
            return color
        else:
            try:
                return TextColors.dict[color]
            except KeyError:
                raise ValueError(f"'{color}' is not a valid color")

    @classmethod
    def hex_to_color(cls, color: str) -> str:
        return TextColors.reverse_dict.get(color, color)

    @classmethod
    def color_to_rgb(cls, color: str) -> tuple:
        hex_color = cls.color_to_hex(color).removeprefix("#")
        return int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)

    @classmethod
    def rgb_to_hex(cls, color: tuple[int, int, int]) -> str:
        return f"#{color[0]:02X}{color[1]:02X}{color[2]:02X}"

    @classmethod
    def rgb_to_color(cls, color: tuple[int, int, int]) -> str:
        hex_color = f"#{color[0]:02X}{color[1]:02X}{color[2]:02X}"
        return TextColors.reverse_dict.get(hex_color, hex_color)

    @classmethod
    def color_to_int(cls, color: str) -> int:
        return int(cls.color_to_hex(color).removeprefix("#"), 16)

    @classmethod
    def int_to_hex(cls, color_int: int) -> str:
        return f"#{color_int:06X}"

    @classmethod
    def int_to_color(cls, color_int: int) -> str:
        hex_color = f"#{color_int:06X}"
        return TextColors.reverse_dict.get(hex_color, hex_color)
