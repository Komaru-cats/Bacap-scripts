overworld_mobs = [
    "allay",
    "armadillo",
    "axolotl",
    "bat",
    "bee",
    "bogged",
    "breeze",
    "camel",
    "cat",
    "cave_spider",
    "chicken",
    "cod",
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
    "ocelot",
    "panda",
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
    "zombie_villager"
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
    "zombified_piglin"
]

end_mobs = [
    "ender_dragon",
    "enderman",
    "endermite",
    "shulker"
]


def iterateThroughMobList(world_mob_list):
    COMPLETE_COLOR = "#00a523"
    INCOMPLETE_COLOR = "#c2c2c2"
    output_mob_list = []

    for mob in world_mob_list:
        output_mob_list.append(f"{mob}Universe")
        print(f'#{mob}')
        print(
            f'data modify storage bacaped_mob_universe_storage {mob}Universe set value {{"translate":"entity.minecraft.{mob}","color":"{INCOMPLETE_COLOR}"}}')
        print(
            f'execute at @s if entity @e[type=minecraft:{mob},distance=..128] run data modify storage bacaped_mob_universe_storage {mob}Universe set value {{"translate":"entity.minecraft.{mob}","color":"{COMPLETE_COLOR}"}}')

    return output_mob_list


def main():
    SEPERATOR_COLOR = "#c2c2c2"
    overworld_mob_list = iterateThroughMobList(sorted(overworld_mobs))
    nether_mob_list = iterateThroughMobList(sorted(nether_mobs))
    end_mob_list = iterateThroughMobList(sorted(end_mobs))

    overworld_colored_text_string = ""
    nether_colored_text_string = ""
    end_colored_text_string = ""

    for mob in overworld_mob_list:
        check_last_mob = overworld_mob_list[-1] if overworld_mob_list else None
        if check_last_mob == mob:
            overworld_colored_text_string += f'{{"translate":"and ","color":"{SEPERATOR_COLOR}"}}, {{"storage":"bacaped_mob_universe_storage","nbt":"{mob}","interpret":true}}'
        else:
            overworld_colored_text_string += f'{{"storage":"bacaped_mob_universe_storage","nbt":"{mob}","interpret":true}},{{"text":", ","color":"{SEPERATOR_COLOR}"}},'

    for mob in nether_mob_list:
        check_last_mob = nether_mob_list[-1] if nether_mob_list else None
        if check_last_mob == mob:
            nether_colored_text_string += f'{{"translate":"and ","color":"{SEPERATOR_COLOR}"}}, {{"storage":"bacaped_mob_universe_storage","nbt":"{mob}","interpret":true}}'
        else:
            nether_colored_text_string += f'{{"storage":"bacaped_mob_universe_storage","nbt":"{mob}","interpret":true}},{{"text":", ","color":"{SEPERATOR_COLOR}"}},'

    for mob in end_mob_list:
        check_last_mob = end_mob_list[-1] if end_mob_list else None
        if check_last_mob == mob:
            end_colored_text_string += f'{{"translate":"and ","color":"{SEPERATOR_COLOR}"}}, {{"storage":"bacaped_mob_universe_storage","nbt":"{mob}","interpret":true}}'
        else:
            end_colored_text_string += f'{{"storage":"bacaped_mob_universe_storage","nbt":"{mob}","interpret":true}},{{"text":", ","color":"{SEPERATOR_COLOR}"}},'

    print(
        f'tellraw @s {{"text":"                                             ","color":"dark_gray","strikethrough":true}}')
    print(
        f'tellraw @s {{"color":"gray","translate":"Mob list for the current dimension of the Mob Universe Advancement"}}')
    print(
        f'tellraw @s {{"text":"                                             ","color":"dark_gray","strikethrough":true}}')

    print(
        f'execute at @s if dimension minecraft:overworld run tellraw @s [{{"translate":"Overworld: ","color":"green"}},{overworld_colored_text_string}]')
    print(
        f'execute at @s if dimension minecraft:the_nether run tellraw @s [{{"translate":"Nether: ","color":"red"}},{nether_colored_text_string}]')
    print(
        f'execute at @s if dimension minecraft:the_end run tellraw @s [{{"translate":"End: ","color":"dark_purple"}},{end_colored_text_string}]')

    print("scoreboard players set @s bacaped_mob_universe 0")


if __name__ == "__main__":
    main()
