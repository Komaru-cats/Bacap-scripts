import re


class FunctionsWritePatterns:
    main = 'function bacaped_rewards:advancement_made_macro {adv_id:"[<adv_path_in_mc>]",reward_id:"[<reward_id_without_namespace>]",tier:"[<adv_type>]"}'
    exp = 'xp add @s [<exp>]\ntellraw @s {"color":"blue","text":" +[<exp>] ","extra":[{"translate":"Experience"}]}'
    msg = 'tellraw @a {"translate":"%1$s has [<message>] %2$s%3$s%4$s","with":[{"selector":"@s"},{"color":"[<color>]","text":"["},{"color":"[<color>]","translate":"[<name>]","hover_event":{"action":"show_text","text":{"color":"[<color>]","translate":"[<name>]","extra":[{"text":"\\n"},{"color":"[<desc_color>]","translate":"[<desc>]"},{"text":"\\n\\n"},{"color":"gray","italic":true,"translate":"%1$s tab","with":[{"translate":"[<tab>]"}]}]}}},{"color":"[<color>]","text":"]"}]}'
    reward_msg = 'tellraw @s {"color":"green","text":" +[<formated_amount>] ","extra":[[<enchantment_name>]{"translate":"[<type>].minecraft.[<item_id>]"}]}'
    enchantment_msg = '{"translate":"[<id>]"},{"text":" [<level>] "},'


class FunctionsReadPatterns:
    give_command = re.compile(
        r"give @\w (?P<item_id>.*?)(?P<components>\[.*?])? (?P<amount>\d+)*"
    )
    summon_command = re.compile(r"summon minecraft:item.*?(?P<nbt>{.*})")
    give_command_trophy = re.compile(
        r"give @\w (?P<item_id>.*?)(?P<components>\[.*])\s*(?P<amount>\d*)"
    )
    summon_command_trophy = re.compile(r"summon minecraft:item.*?(?P<nbt>{.*})")
    exp_command = re.compile(r"xp add @s (\d*)")


class DatapackFunctionsWritePatterns:
    update_score = "execute as @a[advancements={[<adv_path_in_mc>]=true}] run scoreboard players add @s bac_advancements 1"
    update_points = "execute as @a[advancements={[<adv_path_in_mc>]=true}] run scoreboard players operation @s bac_advancements_points += [<adv_type>] bac_points"
    coop_update = "execute if score [<adv_path_in_mc>] bac_obtained matches 1.. run advancement grant @a only [<adv_path_in_mc>]"
    coop_update_team = "execute if score [<adv_path_in_mc>] bac_obtained_[<color_team>] matches 1.. run advancement grant @a[team=bac_team_[<color_team>]] only [<adv_path_in_mc>]"
    grant_trophies = "execute as @s[advancements={[<adv_path_in_mc>]=true}] run function [<reward_namespace>]:trophy/[<reward_path>]"



class BasePatterns:
    #  regex that represents #HEX color code
    color = re.compile(r"#?[A-Fa-f0-9]{6}$")
