# Find out the current size of the world and calculate the difference
execute store result score #wb_current wb_math_temp run worldborder get
$scoreboard players set #wb_target wb_math_temp $(target_blocks)

scoreboard players operation #wb_diff wb_math_temp = #wb_target wb_math_temp
scoreboard players operation #wb_diff wb_math_temp -= #wb_current wb_math_temp

# Protection: If the world is ALREADY greater than or equal to the target, interrupt the script
execute if score #wb_diff wb_math_temp matches ..0 run return 0

# Saving values for macros
# Final target size for the worldborder command
execute store result storage bacap_wb_addon:macro size double 1 run scoreboard players get #wb_target wb_math_temp

# Since wb_diff is in whole blocks, we multiply by 100 before formatting
scoreboard players operation #format_val wb_math_temp = #wb_diff wb_math_temp
scoreboard players operation #format_val wb_math_temp *= #wb_100 wb_math_temp
function bacap_wb_addon:math/format_value

data modify storage bacap_wb_addon:macro size_whole set from storage bacap_wb_addon:temp display_format.w
data modify storage bacap_wb_addon:macro size_frac set from storage bacap_wb_addon:temp display_format.f
data modify storage bacap_wb_addon:macro size_pad set from storage bacap_wb_addon:temp display_format.p