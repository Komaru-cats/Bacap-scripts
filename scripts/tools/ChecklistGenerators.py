import pathlib
from dataclasses import dataclass
from typing import Optional

@dataclass
class ChecklistCategory:
    """
    Holds configuration for a specific checklist category.
    """
    name: str
    mobs: list[str]
    advancement: str
    prefix_json: str
    dimension_req: Optional[str] = None


class BaseChecklistGenerator:
    """
    Base class for generating UI triggers and Advancement checks separately.
    """
    COMPLETE_COLOR = "#00a523"
    INCOMPLETE_COLOR = "#c2c2c2"

    def __init__(self, base_path: pathlib.Path, storage_name: str, trigger_name: str, distance: int, extra_selector: str = ""):
        self.base_path = base_path
        self.storage_name = storage_name
        self.trigger_name = trigger_name
        self.distance = distance
        self.extra_selector = extra_selector

    def _get_selector(self, mob: str) -> str:
        return f"@e[type=minecraft:{mob},distance=..{self.distance}{self.extra_selector}]"

    def _generate_advancement_check_command(self, mobs: list[str], advancement: str) -> str:
        conditions = " ".join([f"if entity {self._get_selector(mob)}" for mob in mobs])
        return f"execute at @s {conditions} run advancement grant @s only {advancement}"

    def _generate_mob_data_commands(self, mob_list: list[str]) -> tuple[list[str], list[str]]:
        keys = []
        commands = []

        for mob in sorted(mob_list):
            key = f"{mob}Check"
            keys.append(key)

            commands.append(f"#{mob}")
            commands.append(
                f'data modify storage {self.storage_name} {key} set value {{"translate":"entity.minecraft.{mob}","color":"{self.INCOMPLETE_COLOR}"}}'
            )
            commands.append(
                f'execute at @s if entity {self._get_selector(mob)} run data modify storage {self.storage_name} {key} set value {{"translate":"entity.minecraft.{mob}","color":"{self.COMPLETE_COLOR}"}}'
            )

        return keys, commands

    def _build_tellraw_json(self, keys: list[str]) -> str:
        parts = []
        for i, key in enumerate(keys):
            storage_part = f'{{"storage":"{self.storage_name}","nbt":"{key}","interpret":true}}'

            if i == len(keys) - 1 and len(keys) > 1:
                parts.append(f'{{"translate":" and ","color":"{self.INCOMPLETE_COLOR}"}}')
                parts.append(storage_part)
            else:
                parts.append(storage_part)
                if i < len(keys) - 2:
                    parts.append(f'{{"text":", ","color":"{self.INCOMPLETE_COLOR}"}}')

        return ",".join(parts)

    def generate_files(self, trigger_filename: str, check_folder: str, categories: list[ChecklistCategory], header_text: str):
        """
        Generates both the UI trigger callback file and the advancement check files in their respective directories.
        """
        # GENERATE TRIGGER CALLBACK
        trigger_dir = self.base_path / "function" / "triggers_callback"
        trigger_dir.mkdir(parents=True, exist_ok=True)
        trigger_path = trigger_dir / trigger_filename

        trigger_lines = []
        tellraws = []

        for cat in categories:
            keys, data_cmds = self._generate_mob_data_commands(cat.mobs)
            trigger_lines.extend(data_cmds)

            tellraw_json = self._build_tellraw_json(keys)

            if cat.dimension_req:
                tellraws.append(f'execute at @s if dimension {cat.dimension_req} run tellraw @s [{cat.prefix_json},{tellraw_json}]')
            else:
                if cat.prefix_json:
                    tellraws.append(f'tellraw @s [{cat.prefix_json},{tellraw_json}]')
                else:
                    tellraws.append(f'tellraw @s [{tellraw_json}]')

        trigger_lines.append(r'tellraw @s {"text":"                                             ","color":"dark_gray","strikethrough":true}')
        trigger_lines.append(f'tellraw @s {{"color":"gray","translate":"{header_text}"}}')
        trigger_lines.append(r'tellraw @s {"text":"                                             ","color":"dark_gray","strikethrough":true}')
        trigger_lines.extend(tellraws)
        trigger_lines.append(f"scoreboard players set @s {self.trigger_name} 0")

        trigger_path.write_text("\n".join(trigger_lines), encoding="utf-8")

        # GENERATE CHECK FILES
        check_dir = self.base_path / "function" / check_folder
        check_dir.mkdir(parents=True, exist_ok=True)

        for cat in categories:
            check_filename = f"{cat.name}_check.mcfunction"
            check_file_path = check_dir / check_filename

            check_cmd = self._generate_advancement_check_command(cat.mobs, cat.advancement)
            check_file_path.write_text(check_cmd, encoding="utf-8")


class MobUniverseGenerator(BaseChecklistGenerator):
    DIMENSIONS = {
        "overworld": {
            "mc_namespace": "minecraft:overworld",
            "color": "green",
            "mobs": [
                "allay", "armadillo", "axolotl", "bat", "bee", "bogged", "breeze",
                "camel", "camel_husk", "cat", "cave_spider", "chicken", "cod",
                "copper_golem", "cow", "creaking", "creeper", "dolphin", "donkey",
                "drowned", "elder_guardian", "evoker", "fox", "frog", "glow_squid",
                "goat", "guardian", "horse", "husk", "iron_golem", "llama",
                "mooshroom", "mule", "nautilus", "ocelot", "panda", "parched",
                "parrot", "phantom", "pig", "pillager", "polar_bear", "pufferfish",
                "rabbit", "ravager", "salmon", "sheep", "silverfish", "skeleton",
                "skeleton_horse", "slime", "sniffer", "snow_golem", "spider",
                "squid", "stray", "sulfur_cube", "tadpole", "trader_llama",
                "tropical_fish", "turtle", "vex", "villager", "vindicator",
                "wandering_trader", "warden", "witch", "wolf", "zombie",
                "zombie_horse", "zombie_nautilus", "zombie_villager"
            ]
        },
        "nether": {
            "mc_namespace": "minecraft:the_nether",
            "color": "red",
            "mobs": [
                "blaze", "ghast", "happy_ghast", "hoglin", "magma_cube",
                "piglin", "piglin_brute", "strider", "wither",
                "wither_skeleton", "zoglin", "zombified_piglin"
            ]
        },
        "end": {
            "mc_namespace": "minecraft:the_end",
            "color": "dark_purple",
            "mobs": ["ender_dragon", "enderman", "endermite", "shulker"]
        }
    }

    def __init__(self, base_path: pathlib.Path):
        super().__init__(
            base_path=base_path,
            storage_name="bacaped_mob_universe_storage",
            trigger_name="bacaped_mob_universe",
            distance=128,
            extra_selector=""
        )

    def generate_all_files(self):
        categories = []
        for dim_name, data in self.DIMENSIONS.items():
            dim_title = dim_name.capitalize()
            prefix_json = f'{{"translate":"{dim_title}: ","color":"{data["color"]}"}}'

            categories.append(
                ChecklistCategory(
                    name=dim_name,
                    mobs=data["mobs"],
                    advancement=f"bacaped:challenges/mob_universe {dim_name}",
                    prefix_json=prefix_json,
                    dimension_req=data["mc_namespace"]
                )
            )

        self.generate_files(
            trigger_filename="mob_universe_trigger.mcfunction",
            check_folder="mob_universe",
            categories=categories,
            header_text="Mob list for the current dimension of the Mob Universe Advancement"
        )


class BabyZooGenerator(BaseChecklistGenerator):
    MOBS = [
        "armadillo", "axolotl", "bee", "camel", "cat", "chicken", "cow", "dolphin",
        "donkey", "fox", "glow_squid", "goat", "happy_ghast", "hoglin", "horse",
        "llama", "mooshroom", "mule", "nautilus", "ocelot", "panda", "pig",
        "polar_bear", "rabbit", "sheep", "sniffer", "squid", "strider", "turtle", "wolf"
    ]

    def __init__(self, base_path: pathlib.Path):
        super().__init__(
            base_path=base_path,
            storage_name="bacaped_baby_zoo_storage",
            trigger_name="bacaped_baby_zoo",
            distance=32,
            extra_selector=",predicate=bacaped:is_baby"
        )

    def generate_all_files(self):
        category = ChecklistCategory(
            name="baby_zoo",
            mobs=self.MOBS,
            advancement="bacaped:animal/baby_zoo",
            prefix_json=''
        )

        self.generate_files(
            trigger_filename="baby_zoo_trigger.mcfunction",
            check_folder="mob_collections",
            categories=[category],
            header_text="Baby Zoo list"
        )