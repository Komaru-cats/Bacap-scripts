overworld_mobs = [
    "allay",
    "armadillo",
    "axolotl",
    "bat",
    "bee",
    "bogged",
    "breeze",
    "camel",
    "camel_husk",
    "cat",
    "cave_spider",
    "chicken",
    "cod",
    "copper_golem",
    "cow",
    "creaking",
    "creeper",
    "dolphin",
    "donkey",
    "drowned",
    "elder_guardian",
    "evoker",
    "fox",
    "frog",
    "glow_squid",
    "goat",
    "guardian",
    "horse",
    "husk",
    "iron_golem",
    "llama",
    "mooshroom",
    "mule",
    "nautilus",
    "ocelot",
    "panda",
    "parched",
    "parrot",
    "phantom",
    "pig",
    "pillager",
    "polar_bear",
    "pufferfish",
    "rabbit",
    "ravager",
    "salmon",
    "sheep",
    "silverfish",
    "skeleton",
    "skeleton_horse",
    "slime",
    "sniffer",
    "snow_golem",
    "spider",
    "squid",
    "stray",
    "sulfur_cube",
    "tadpole",
    "trader_llama",
    "tropical_fish",
    "turtle",
    "vex",
    "villager",
    "vindicator",
    "wandering_trader",
    "warden",
    "witch",
    "wolf",
    "zombie",
    "zombie_horse",
    "zombie_nautilus",
    "zombie_villager",
]

nether_mobs = [
    "blaze",
    "ghast",
    "happy_ghast",
    "hoglin",
    "magma_cube",
    "piglin",
    "piglin_brute",
    "strider",
    "wither",
    "wither_skeleton",
    "zoglin",
    "zombified_piglin",
]

end_mobs = ["ender_dragon", "enderman", "endermite", "shulker"]


def generate_trigger_command(mobs, dimension_name):
    conditions = " ".join(
        [f"if entity @e[type=minecraft:{mob},distance=..128]" for mob in mobs]
    )
    return f"execute at @s {conditions} run advancement grant @s only bacaped:challenges/mob_universe {dimension_name}"


def generate_mob_data_commands(mob_list: list[str]):
    COMPLETE_COLOR = "#00a523"
    INCOMPLETE_COLOR = "#c2c2c2"

    keys = []
    commands = []

    for mob in sorted(mob_list):
        key = f"{mob}Universe"
        keys.append(key)

        commands.append(f"#{mob}")
        commands.append(
            f'data modify storage bacaped_mob_universe_storage {key} set value {{"translate":"entity.minecraft.{mob}","color":"{INCOMPLETE_COLOR}"}}'
        )
        commands.append(
            f'execute at @s if entity @e[type=minecraft:{mob},distance=..128] run data modify storage bacaped_mob_universe_storage {key} set value {{"translate":"entity.minecraft.{mob}","color":"{COMPLETE_COLOR}"}}'
        )

    return keys, commands


def build_tellraw_json(keys):
    seperator_color = "#c2c2c2"
    parts = []

    for i, key in enumerate(keys):
        storage_part = f'{{"storage":"bacaped_mob_universe_storage","nbt":"{key}","interpret":true}}'
        if i == len(keys) - 1 and len(keys) > 1:
            parts.append(f'{{"translate":"and ","color":"{seperator_color}"}}')
            parts.append(storage_part)
        else:
            parts.append(storage_part)
            if i < len(keys) - 1:
                parts.append(f'{{"text":", ","color":"{seperator_color}"}}')

    return ",".join(parts)


def main():
    # Tellraw:
    output_lines = []

    ow_keys, ow_cmds = generate_mob_data_commands(overworld_mobs)
    nether_keys, nether_cmds = generate_mob_data_commands(nether_mobs)
    end_keys, end_cmds = generate_mob_data_commands(end_mobs)

    output_lines.extend(ow_cmds)
    output_lines.extend(nether_cmds)
    output_lines.extend(end_cmds)

    output_lines += [
        r'tellraw @s {"text":"                                             ","color":"dark_gray","strikethrough":true}',
        r'tellraw @s {"color":"gray","translate":"Mob list for the current dimension of the Mob Universe Advancement"}',
        r'tellraw @s {"text":"                                             ","color":"dark_gray","strikethrough":true}',
        f'execute at @s if dimension minecraft:overworld run tellraw @s [{{"translate":"Overworld: ","color":"green"}},{build_tellraw_json(ow_keys)}]',
        f'execute at @s if dimension minecraft:the_nether run tellraw @s [{{"translate":"Nether: ","color":"red"}},{build_tellraw_json(nether_keys)}]',
        f'execute at @s if dimension minecraft:the_end run tellraw @s [{{"translate":"End: ","color":"dark_purple"}},{build_tellraw_json(end_keys)}]',
    ]

    output_lines.append("scoreboard players set @s bacaped_mob_universe 0")

    print("\n".join(output_lines))

    # Trigger command:
    print("\n\nTRIGGER COMMAND:")
    print(generate_trigger_command(overworld_mobs, "overworld"))
    print(generate_trigger_command(nether_mobs, "nether"))
    print(generate_trigger_command(end_mobs, "end"))


if __name__ == "__main__":
    main()
