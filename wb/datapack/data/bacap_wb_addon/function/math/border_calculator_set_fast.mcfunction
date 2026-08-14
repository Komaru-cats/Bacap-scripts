# Find out the current size of the world and calculate the difference
execute store result score #wb_current wb_math_temp run worldborder get
$scoreboard players set #wb_target wb_math_temp $(target_blocks)

scoreboard players operation #wb_diff wb_math_temp = #wb_target wb_math_temp
scoreboard players operation #wb_diff wb_math_temp -= #wb_current wb_math_temp

# Protection: If the world is ALREADY greater than or equal to the target, interrupt the script
execute if score #wb_diff wb_math_temp matches ..0 run return 0

# Saving values for macros
# For the worldborder set command, we need the final size (#wb_target)
execute store result storage bacap_wb_addon:macro size double 1 run scoreboard players get #wb_target wb_math_temp

# For the chat message we need the difference (how many blocks were added)
execute store result storage bacap_wb_addon:macro size_whole int 1 run scoreboard players get #wb_diff wb_math_temp
data modify storage bacap_wb_addon:macro size_frac set value 0
data modify storage bacap_wb_addon:macro size_pad set value "0"