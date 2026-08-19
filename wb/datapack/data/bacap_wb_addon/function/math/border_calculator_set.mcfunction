# Find out the current size of the world and calculate the difference
execute store result score #wb_current wb_math_temp run worldborder get
$scoreboard players set #wb_target wb_math_temp $(target_blocks)

scoreboard players operation #wb_diff wb_math_temp = #wb_target wb_math_temp
scoreboard players operation #wb_diff wb_math_temp -= #wb_current wb_math_temp

# Protection: If the world is ALREADY greater than or equal to the target, interrupt the script
execute if score #wb_diff wb_math_temp matches ..0 run return 0

# Saving values for macros
# For the worldborder set command, we need the final size (#wb_target in whole blocks, so multiplier is 1)
execute store result storage bacap_wb_addon:macro size double 1 run scoreboard players get #wb_target wb_math_temp

# Since wb_diff is in whole blocks, we MUST multiply it by 100 before passing
# to the formatter to display properly (e.g. 50 -> 5000 -> "50.00")
scoreboard players operation #format_val wb_math_temp = #wb_diff wb_math_temp
scoreboard players operation #format_val wb_math_temp *= #wb_100 wb_math_temp
function bacap_wb_addon:math/format_value

data modify storage bacap_wb_addon:macro size_whole set from storage bacap_wb_addon:temp display_format.w
data modify storage bacap_wb_addon:macro size_frac set from storage bacap_wb_addon:temp display_format.f
data modify storage bacap_wb_addon:macro size_pad set from storage bacap_wb_addon:temp display_format.p

# Preparing for Newton
scoreboard players operation #wb_sq wb_math_temp = #wb_diff wb_math_temp
function bacap_wb_addon:math/newton_sqrt

# Convert the root to ticks (speed matched to regular advancements)
scoreboard players operation #wb_R wb_math_temp *= #wb_40 wb_math_temp
scoreboard players add #wb_R wb_math_temp 1

# Save time in a macro
execute store result storage bacap_wb_addon:macro time int 1 run scoreboard players get #wb_R wb_math_temp