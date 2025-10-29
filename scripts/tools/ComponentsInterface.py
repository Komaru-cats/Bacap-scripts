import json
from typing import Dict, Any
from . import Resources
from .InterfaceSchema import *
from .utils import cut_namespace, arabic_to_rims, merge_dicts
from .Color import Color


class BasicComponent:
    custom_lore: bool


class ComponentsInterface:
    """
    Class for Interface to input item components.
    Return components (dict)
    """
    components_list = []

    @classmethod
    def register(cls, comp_cls):
        cls.components_list.append(comp_cls)
        return comp_cls

    def __new__(cls, item_id, add_lore: bool = False, indent: int = 0) -> Dict[str, Any]:
        """

        :param item_id: The id of mc item.
        :param add_lore: Does add custom lore to components
        :param indent: Indent of console input/output.
        """
        if item_id not in Resources.ItemProperties.list:
            raise ValueError(f"Can't find item {item_id}")
        components = {}
        lore = []

        def add_comp(comp_cls):
            output(comp_cls.__name__, indent=indent)
            comp_cls.custom_lore = add_lore
            comp_obj = comp_cls(indent + 3)
            merge_dicts(components, comp_obj.component)
            if hasattr(comp_obj, "lore") and comp_obj.lore:
                lore.extend(comp_obj.lore)

        for component_class in cls.components_list:
            if hasattr(component_class, "always_set") and component_class.always_set:
                add_comp(component_class)

            elif (not component_class.items or item_id in component_class.items) and (
                    item_id not in component_class.excluded_items):
                if get_bool(f"Set {component_class.__name__} [y/n]:", icon=Icon(icon="[>]", color="yellow"),
                            indent=indent):
                    add_comp(component_class)
        if add_lore and components:
            components["lore"] = lore
        return components


@ComponentsInterface.register
class Profile(BasicComponent):
    items = ("player_head",)
    excluded_items = ()

    def __init__(self, indent):
        self.indent = indent
        self.component = self.input_component()

    def input_component(self):
        import re
        from pyperclip import paste as pypaste
        pattern = re.compile(
            r"profile\"?[:=]{id:\[I;(?P<id>.*?)],properties:\[{name:\"textures\",value:\"(?P<value>.*?)\"}")
        search = None
        output("https://minecraft-heads.com/wiki/heads/heads-categories", indent=self.indent)
        while not search:
            get_value("Copy the command to the clipboard and continue [any]:", indent=self.indent)
            search = re.search(pattern, pypaste())
        search = search.groupdict()
        output("PlayerHead has been parsed", indent=self.indent)
        return {
            "profile": {
                "id": list(map(int, search["id"].split(","))),
                "properties": [
                    {
                        "name": "textures",
                        "value": search["value"]
                    }
                ]
            }
        }


@ComponentsInterface.register
class Trim(BasicComponent):
    items = ('leather_boots', 'leather_chestplate', 'leather_helmet', 'leather_leggings', 'chainmail_boots',
             'chainmail_chestplate',
             'chainmail_helmet', 'chainmail_leggings', 'iron_boots', 'iron_chestplate', 'iron_helmet', 'iron_leggings',
             'golden_boots',
             'golden_chestplate', 'golden_helmet', 'golden_leggings', 'diamond_boots', 'diamond_chestplate',
             'diamond_helmet', 'diamond_leggings',
             'netherite_boots', 'netherite_chestplate', 'netherite_helmet', 'netherite_leggings', 'turtle_helmet')
    excluded_items = ()
    trim_material_colors = Resources.TrimMaterialColor.dict
    trim_list = Resources.TrimList.list

    def __init__(self, indent):
        self.trim_pattern = None
        self.trim_material = None
        self.indent = indent
        self.show_in_tooltip = get_bool("Show in tooltip [y/n]:", indent=self.indent)
        self.component = self.input_component()
        if self.custom_lore and self.show_in_tooltip:
            self.lore = self.create_lore()

    def input_component(self):
        output("Trims: " + ", ".join(self.trim_list), indent=self.indent)
        self.trim_pattern = get_value("Trim:", possible_value=self.trim_list, indent=self.indent)
        self.trim_material = get_value("Material:", possible_value=self.trim_material_colors.keys(), indent=self.indent)
        comp = {
            "tooltip_display": {"hidden_components": []},
            "trim":
                {
                    "material": self.trim_material,
                    "pattern": self.trim_pattern
                }
        }
        if not self.show_in_tooltip or self.custom_lore:
            comp["tooltip_display"]["hidden_components"].append("minecraft:trim")
        return comp

    def create_lore(self):
        trim_color = self.trim_material_colors[self.trim_material]
        lore = [
            {
                "translate": "item.minecraft.smithing_template.upgrade",
                "color": "gray",
                "italic": False},
            {
                "translate": " ",
                "extra": [
                    {
                        "translate": f"trim_pattern.minecraft.{self.trim_pattern}",
                        "color": trim_color,
                        "italic": False
                    }
                ]
            },
            {
                "translate": " ",
                "extra": [
                    {
                        "translate": f"trim_material.minecraft.{self.trim_material}",
                        "color": trim_color,
                        "italic": False
                    }
                ]
            }
        ]
        return lore


class BasicEnchantments(BasicComponent):

    def __init__(self, indent):
        self.indent = indent
        self.lore = None
        self.show_in_tooltip = None
        self.levels = None
        self.input_levels()

    def input_levels(self):
        while True:
            levels = {}

            while True:
                enchantment = get_value("Enchantment:", possible_value=Resources.Enchantments.list + [""],
                                        indent=self.indent)
                if enchantment == "":
                    break
                else:
                    levels[enchantment] = get_value("Level:", value_type=int, indent=self.indent)
            output("Enchantments:\n" + json.dumps(levels, indent=1), indent=self.indent)
            if get_bool("Continue with these enchantments [y/n]:", indent=self.indent):
                self.show_in_tooltip = get_bool("Show in tooltip [y/n]:", indent=self.indent)
                if self.custom_lore and self.show_in_tooltip:
                    self.lore = self.create_lore(levels)
                self.levels = levels
                return

    @staticmethod
    def create_lore(levels):
        lore = []
        for enchantment, level in levels.items():
            enchantment = cut_namespace(enchantment)
            lore.append(
                {"translate": f"enchantment.minecraft.{enchantment}",
                 "color": "gray",
                 "italic": False,
                 "extra":
                     [
                         {"text": f" {arabic_to_rims(level) if level > 1 else ""}",
                          "color": "#FC5454" if enchantment in Resources.Enchantments.curses else "gray",
                          "italic": False}
                     ]
                 })
        return lore


@ComponentsInterface.register
class StoredEnchantments(BasicEnchantments):
    items = ("enchanted_book",)
    excluded_items = ()

    def __init__(self, indent):
        self.indent = indent
        super().__init__(indent)
        self.component = self.input_component()

    def input_component(self):
        comp = {
            "tooltip_display": {"hidden_components": []},
            "stored_enchantments": self.levels
        }
        if not self.show_in_tooltip or self.custom_lore:
            comp["tooltip_display"]["hidden_components"].append("minecraft:stored_enchantments")
        return comp


@ComponentsInterface.register
class ItemEnchantments(BasicEnchantments):
    items = ()
    excluded_items = ("enchanted_book",)

    def __init__(self, indent):
        self.indent = indent
        super().__init__(indent)
        self.component = self.input_component()

    def input_component(self):
        comp = {
            "tooltip_display": {"hidden_components": []},
            "enchantments": self.levels
        }
        if not self.show_in_tooltip or self.custom_lore:
            comp["tooltip_display"]["hidden_components"].append("minecraft:enchantments")
        return comp


@ComponentsInterface.register
class EnchantmentGlintOverride(BasicComponent):
    always_set = True
    items = ()
    excluded_items = ()

    def __init__(self, indent):
        self.indent = indent
        self.component = self.input_component()

    def input_component(self):
        return {"enchantment_glint_override": get_bool("Glint [y/n]:", indent=self.indent)}


@ComponentsInterface.register
class DyedColor(BasicComponent):
    items = ("leather_boots", "leather_chestplate", "leather_helmet", "leather_horse_armor", "leather_leggings",
             "wolf_armor")
    excluded_items = ()

    def __init__(self, indent):
        self.indent = indent
        while True:
            try:
                self.color = get_value("Hex color:", indent=self.indent, function_to_check=Color.color_to_int)
                break
            except ValueError:
                continue
        self.show_in_tooltip = get_bool("Show in tooltip [y/n]:", indent=self.indent)
        self.component = self.input_component()
        if self.custom_lore and self.show_in_tooltip:
            self.lore = self.create_lore()

    def input_component(self) -> Dict:
        comp = {
            "tooltip_display": {"hidden_components": []},
            "dyed_color": Color.color_to_int(self.color)
        }
        if not self.show_in_tooltip or self.custom_lore:
            comp["tooltip_display"]["hidden_components"].append("minecraft:dyed_color")
        return comp

    def create_lore(self):
        lore = [
            {
                "translate": "item.color",
                "with": [self.color],
                "color": "gray",
                "italic": False
            }
        ]
        return lore


class BookContent(BasicComponent):
    def __init__(self, indent):
        self.indent = indent

    def input_pages(self):
        import textwrap
        from pyperclip import paste as pypaste
        get_value("Copy text to clipboard and continue [any]:", indent=self.indent)
        paste_text = pypaste()
        pages = textwrap.wrap(paste_text, width=256, max_lines=100)
        output(f"Text pasted:\nPages: {len(pages)}\nChars: {len(paste_text)}", indent=self.indent)
        return [{"translate": page} for page in pages]


@ComponentsInterface.register
class WrittenBookContent(BookContent):
    items = ("written_book",)
    excluded_items = ()

    def __init__(self, indent):
        self.indent = indent
        super().__init__(indent)
        self.component = self.input_pages()

    def input_pages(self):
        comp = {
            "written_book_content":
                {
                    "pages": super().input_pages(),
                    "author": get_value("Author:", indent=self.indent),
                    "title": get_value("Title:", indent=self.indent),
                    "generation": get_value("Generation (0 is original) [0-3]:", int, possible_value=(0, 1, 2, 3),
                                            indent=self.indent)
                }
        }
        return comp


@ComponentsInterface.register
class WritableBookContent(BookContent):
    items = ("writable_book",)
    excluded_items = ()

    def __init__(self, indent):
        self.indent = indent
        super().__init__(indent)
        self.component = self.input_pages()

    def input_pages(self):
        comp = {
            "writable_book_content": {
                "pages": super().input_pages()
            }
        }
        return comp


@ComponentsInterface.register
class Bees(BasicComponent):
    items = ("beehive", "bee_nest")
    excluded_items = ()

    def __init__(self, indent):
        self.indent = indent
        self.component = self.input_component()

    def input_component(self):
        comp = {"bees": []}
        bee_data = {
            "ticks_in_hive": 0,
            "min_ticks_in_hive": 0,
            "entity_data": {"id": "minecraft:bee"}
        }
        comp["bees"] = [bee_data] * get_value("Bee count:", value_type=int, indent=self.indent)
        return comp


@ComponentsInterface.register
class OminusBottleAmplifier(BasicComponent):
    items = ("minecraft:ominous_bottle",)
    excluded_items = ()

    def __init__(self, indent):
        self.component = self.input_component()
        self.indent = indent

    def input_component(self):
        comp = {"ominous_bottle_amplifier": get_value("Ominus Level:", value_type=int, indent=self.indent)}
        return comp


@ComponentsInterface.register
class SuspiciousStewEffects(BasicComponent):
    items = ("suspicious_stew",)
    excluded_items = ()

    def __init__(self, indent):
        self.indent = indent
        self.component = self.input_component()

    def input_component(self):
        effect_id = get_value("Effect:", possible_value=Resources.Effects.list, indent=self.indent)
        ticks = int(get_value("Seconds:", value_type=float, indent=3) * 20)
        comp = {"suspicious_stew_effects": [{"duration": ticks, "id": effect_id}]}
        return comp


@ComponentsInterface.register
class Instrument(BasicComponent):
    items = ("goat_horn",)
    excluded_items = ()

    def __init__(self, indent):
        self.indent = indent
        self.component = self.input_component()

    def input_component(self):
        instrument_list = ("admire_goat_horn", "call_goat_horn", "dream_goat_horn", "feel_goat_horn",
                           "ponder_goat_horn", "seek_goat_horn", "sing_goat_horn", "yearn_goat_horn")
        output(f"Possible values:\n{", ".join(instrument_list)}", indent=self.indent)
        comp = {"instrument": get_value("Instrument:", possible_value=instrument_list, indent=self.indent)}
        return comp


@ComponentsInterface.register
class BaseColor(BasicComponent):
    items = ("shield",)
    excluded_items = ()

    def __init__(self, indent):
        self.indent = indent
        self.component = self.input_component()

    def input_component(self):
        return {"base_color": get_value("Color:", possible_value=Resources.DyeColors.list, indent=self.indent)}


@ComponentsInterface.register
class BannerPatterns(BasicComponent):
    items = ('black_banner', 'blue_banner', 'brown_banner', 'cyan_banner', 'gray_banner', 'green_banner',
             'light_blue_banner', 'light_gray_banner', 'lime_banner',
             'magenta_banner', 'orange_banner', 'pink_banner', 'purple_banner', 'red_banner', 'white_banner',
             'yellow_banner', 'shield')

    excluded_items = ()
    pattern_list = Resources.BannerPatterns.list

    def __init__(self, indent):
        self.indent = indent
        self.component = self.input_component()

    def input_component(self):
        patterns = []
        while True:
            pattern = get_value("Pattern:", possible_value=self.pattern_list + [""], indent=self.indent)
            if not pattern:
                break
            patterns.append({"color": get_value("Color:", possible_value=Resources.DyeColors.list, indent=self.indent),
                             "pattern": pattern})
        comp = {
            "tooltip_display": {"hidden_components": []},
            "banner_patterns": patterns
        }
        if not get_bool("Show in tooltip [y/n]:", indent=self.indent):
            comp["tooltip_display"]["hidden_components"].append("minecraft:banner_patterns")
        return comp


class FireworkExplosionBase(BasicComponent):
    dye_colors = Resources.DyeColors.dict
    possible_shapes = Resources.FireworkShapes.list

    def __init__(self, indent):
        self.indent_expl_base = indent

    def __get_list_color(self):
        color_list = []
        if get_bool("Custom color or vanilla-color list [c/v]:", true_values="c", false_values="v",
                    indent=self.indent_expl_base):
            color_list.append(
                get_value("Custom color:", value_type=Color.color_to_int, indent=self.indent_expl_base + 3))
        else:
            while True:
                color = get_value("Color:", possible_value=set(self.dye_colors.keys()) | {"", },
                                  indent=self.indent_expl_base + 3)
                if not color:
                    break
                color_list.append(color)
                output("Colors: " + ", ".join(color_list), indent=self.indent_expl_base + 3)
            color_list = [self.dye_colors[color] for color in color_list]
        return color_list

    def input_explosion(self):
        output(f"Possible shapes:\n" + ", ".join(self.possible_shapes), indent=self.indent_expl_base)
        shape = get_value("Shape:", possible_value=self.possible_shapes, indent=self.indent_expl_base)
        colors = self.__get_list_color()
        fade_colors = None
        if get_bool("Fade color [y/n]:", indent=self.indent_expl_base):
            fade_colors = self.__get_list_color()

        comp = {

            "shape": shape,
            "colors": colors,
            "has_trail": get_bool("Trial [y/n]:", indent=self.indent_expl_base),
            "has_twinkle": get_bool("Twinkle [y/n]:", indent=self.indent_expl_base)
        }
        if fade_colors:
            comp["fade_colors"] = fade_colors
        return comp


@ComponentsInterface.register
class FireworkExplosion(FireworkExplosionBase):
    items = ("firework_star",)
    excluded_items = ()

    def __init__(self, indent):
        self.indent = indent
        super().__init__(indent)
        self.component = self.input_component()

    def input_component(self):
        return {"firework_explosion": super().input_explosion()}


@ComponentsInterface.register
class Fireworks(FireworkExplosionBase):
    items = ("firework_rocket",)
    excluded_items = ()

    def __init__(self, indent):
        self.indent = indent
        super().__init__(indent + 3)
        self.show_in_tooltip = get_bool("Show in tooltip [y/n]:", indent=self.indent)
        self.component = self.input_component()

    def input_component(self):
        explosions = []
        while get_bool("Add explosion [y/n]:", indent=self.indent):
            explosions.append(super().input_explosion())
        comp = {
            "tooltip_display": {"hidden_components": []},
            "fireworks": {
                "explosions": explosions,
                "flight_duration": get_value("Flight duration:", int, indent=self.indent)
            }
        }
        if not self.show_in_tooltip or self.custom_lore:
            comp["tooltip_display"]["hidden_components"].append("minecraft:fireworks")
        return comp


class ContainerBasic(BasicComponent):
    items = Resources.Containers.list


@ComponentsInterface.register
class Container(ContainerBasic):
    excluded_items = ()

    def __init__(self, indent):
        self.indent = indent
        self.component = self.input_component()

    def input_component(self):
        from math import ceil
        item_id = get_value("Item id:", possible_value=Resources.ItemProperties.list, indent=self.indent)
        item_stack_size = Resources.ItemProperties.dict[item_id]["stack_size"]
        item_count = get_value("Item count in container:", int, indent=self.indent)
        components = {}
        if get_bool("Add components to this item [y/n]:", indent=self.indent):
            components = ComponentsInterface(item_id, indent=self.indent + 3)
        return {
            "container": [{"slot": slot, "item": {"id": item_id, "count": (
                min(item_stack_size, item_count - (slot * item_stack_size))), "components": components}}
                          for slot in range(ceil(item_count / item_stack_size))]
        }


@ComponentsInterface.register
class ContainerLoot(ContainerBasic):
    excluded_items = ()

    def __init__(self, indent):
        self.indent = indent
        self.component = self.input_component()

    @staticmethod
    def input_component():
        return {"container_loot": {"loot_table": get_value("Loot Table:")}}


@ComponentsInterface.register
class LodestoneTracker:
    items = ("compass",)
    excluded_items = ()

    def __init__(self, indent):
        self.indent = indent
        self.component = self.input_component()

    def input_component(self):
        lodestone_tracker = {"tracked": get_bool("Tracked [y/n]:", indent=self.indent)}

        if get_bool("Add coordinates [y/n]:", indent=self.indent):
            x, y, z = get_value("X:", int, indent=self.indent), get_value("Y:", int, indent=self.indent), get_value(
                "Z:", int, indent=self.indent)
            dimension = get_value("Dimension:",
                                  possible_values=("minecraft:overworld", "minecraft:the_nether", "minecraft:the_end"),
                                  indent=self.indent)
            lodestone_tracker["target"] = {"pos": [x, y, z], "dimension": dimension}
        return {"minecraft:lodestone_tracker": lodestone_tracker}


@ComponentsInterface.register
class BundleContents(BasicComponent):
    items = ("bundle",)
    excluded_items = ()

    def __init__(self, indent):
        self.indent = indent
        self.component = self.input_component()

    def input_component(self):
        container = []
        while get_bool("Add Item [y/n]:", indent=self.indent):
            item_id = get_value("Item id:", possible_value=Resources.ItemProperties.list, indent=self.indent + 3)
            item_count = get_value("Item count in container:", int, indent=self.indent + 3)
            components = {}
            if get_bool("Add components to this item [y/n]:", indent=self.indent + 3):
                components = ComponentsInterface(item_id, indent=self.indent + 6)
            container.append({"id": item_id, "count": item_count, "components": components})
        return {
            "bundle_contents": container
        }


@ComponentsInterface.register
class ChargedProjectiles(BasicComponent):
    items = ("crossbow",)
    excluded_items = ()

    def __init__(self, indent):
        self.indent = indent
        self.component = self.input_component()

    def input_component(self):
        container = []
        output("For a crossbow, you can add any number of projectiles", indent=self.indent)
        while get_bool("Add Projectile [y/n]:", indent=self.indent):
            item_id = get_value("Projectile id:", indent=self.indent + 3, possible_value=Resources.ItemProperties.list)
            item_count = get_value("Count of this projectile:", int, indent=self.indent + 3)
            components = {}
            if get_bool("Add components to this projectile [y/n]:", indent=self.indent + 3):
                components = ComponentsInterface(item_id, indent=self.indent + 6)
            container.extend([{"id": item_id, "components": components}] * item_count)
        return {
            "charged_projectiles": container
        }


@ComponentsInterface.register
class PotionContents(BasicComponent):
    items = ("tipped_arrow", "splash_potion", "lingering_potion", "potion")
    excluded_items = ()
    potion_data = Resources.Potion.dict
    effects = Resources.Effects.list

    def __init__(self, indent):
        self.indent = indent
        self.component = self.input_component()

    def input_component(self):
        potion = None
        custom_color = None
        output("You can set any potion (one) and/or effects (any amount)", indent=self.indent)
        if get_bool("Add custom potion [y/n]:", indent=self.indent):
            potion = get_value("Potion:", possible_value=(self.potion_data.keys()), indent=self.indent + 3)
            possible = [prop[0] for prop in self.potion_data[potion].items() if prop[1]]
            if possible:
                keys = {prop[0]: prop + "_" for prop in possible}
                msg = " or ".join(
                    [prop.capitalize() for prop in possible] + ["Normal"]) + f" [{"/".join(keys.keys())}/n]:"
                potion = get_value_from_variants(msg, **keys, n="", indent=self.indent + 3) + potion

        if get_bool("Add custom color [y/n]:", indent=self.indent):
            custom_color = get_value("Custom color:", value_type=Color.color_to_int, indent=self.indent + 3)

        custom_effects = []
        while get_bool("Add effect [y/n]:", indent=self.indent):
            custom_effects.append({"id": get_value("Effect:", possible_value=self.effects, indent=self.indent + 3),
                                   "amplifier": get_value("Amplifier:", int, indent=self.indent + 3),
                                   "duration": get_value("Duration [seconds]:", int, indent=self.indent + 3) * 20,
                                   "show_particles": get_bool("Show particle [y/n]:", indent=self.indent + 3)
                                   })
        comp = {}
        if potion:
            comp["potion"] = potion
        if custom_color:
            comp["custom_color"] = custom_color
        if custom_effects:
            comp["custom_effects"] = custom_effects
        return {"potion_contents": comp}


@ComponentsInterface.register
class PotDecoration(BasicComponent):
    items = ("decorated_pot",)
    excluded_items = ()
    possible_sherds = (
        "brick", "angler", "archer", "arms_up", "blade", "brewer", "burn", "danger", "explorer", "flow", "friend",
        "guster", "heart",
        "heartbreak", "howl", "miner", "mourner", "plenty", "prize", "scrape", "sheaf", "shelter", "skull", "snort")

    def __init__(self, indent):
        self.indent = indent
        self.component = self.input_component()

    def input_component(self):
        output("Possible sherds: " + ", ".join(self.possible_sherds), indent=self.indent)
        sherds = []
        for _ in range(4):
            sherd = get_value("Sherd:", possible_value=self.possible_sherds, indent=self.indent)
            if sherd != "brick":
                sherd = sherd + "_pottery_sherd"
            sherds.append(sherd)
            output("Sherds: " + ", ".join(sherds), indent=self.indent)
        return {"pot_decorations": sherds}


@ComponentsInterface.register
class AttributeModifier(BasicComponent):
    items = ()
    excluded_items = ()
    possible_modifiers = (
        'minecraft:armor.body', 'minecraft:armor.boots', 'minecraft:armor.chestplate', 'minecraft:armor.helmet',
        'minecraft:armor.leggings', 'minecraft:attacking', 'minecraft:baby',
        'minecraft:base_attack_damage', 'minecraft:base_attack_speed', 'minecraft:covered', 'minecraft:drinking',
        'minecraft:effect.haste', 'minecraft:effect.health_boost',
        'minecraft:effect.jump_boost', 'minecraft:effect.luck', 'minecraft:effect.mining_fatigue',
        'minecraft:effect.slowness', 'minecraft:effect.speed',
        'minecraft:effect.strength', 'minecraft:effect.unluck', 'minecraft:effect.weakness',
        'minecraft:leader_zombie_bonus', 'minecraft:powder_snow', 'minecraft:random_spawn_bonus',
        'minecraft:reinforcement_callee_charge', 'minecraft:reinforcement_caller_charge', 'minecraft:sprinting',
        'minecraft:zombie_random_spawn_bonus'

    )
    possible_slots = ("any", "armor", "body", "chest", "feet", "hand", "head", "legs", "mainhand", "offhand")

    def __init__(self, indent):
        self.indent = indent
        self.component = self.input_component()

    def input_component(self):
        modifiers = []
        while get_bool("Add modifiers [y/n]:", indent=self.indent):
            modifier = {
                "type": get_value("Modifier:", possible_value=self.possible_modifiers, indent=self.indent + 3),
                "operation": get_value("Operation:",
                                       possible_value=("add_multiplied_base", "add_multiplied_total", "add_value"),
                                       indent=self.indent + 3),
                "amount": get_value("Amount:", float, indent=self.indent + 3),
                "id": "",
                "slot": get_value("Slot:", possible_value=self.possible_slots, indent=self.indent + 3)}
            modifiers.append(modifier)
        comp = {
            "tooltip_display": {"hidden_components": []},
            "attribute_modifiers": modifiers
        }
        if not get_bool("Show in tooltip [y/n]:", indent=self.indent):
            comp["tooltip_display"]["hidden_components"].append("minecraft:attribute_modifiers")
        return comp


@ComponentsInterface.register
class Unbreakable(BasicComponent):
    items = ()
    excluded_items = ()

    def __init__(self, indent):
        self.indent = indent
        self.component = self.input_component()

    def input_component(self):
        comp = {"tooltip_display": {"hidden_components": []}, "unbreakable": {}}
        if not get_bool("Show in tooltip [y/n]:", indent=self.indent):
            comp["tooltip_display"]["hidden_components"].append("minecraft:unbreakable")
        return comp


@ComponentsInterface.register
class FireResistant(BasicComponent):
    items = ()
    excluded_items = ()

    def __init__(self, indent):
        self.indent = indent
        self.component = {"damage_resistant": {"types": "#minecraft:is_fire"}}


""
