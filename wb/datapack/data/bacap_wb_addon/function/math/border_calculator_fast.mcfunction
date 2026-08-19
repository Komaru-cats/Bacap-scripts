# Capture the passed number in a temporary variable #wb_base
$scoreboard players set #wb_base wb_math_temp $(blocks)

# Applying a multiplier SAFELY
execute store result score #wb_mult wb_math_temp run data get storage bacap_wb_addon:settings mult_int 1

# Step A: Get the whole part and multiply it (ЗАЩИТА ОТ КАСТОМА)
execute unless data storage bacap_wb_addon:queue current_task{tier:"custom"} run scoreboard players operation #wb_whole wb_math_temp = #wb_base wb_math_temp
execute unless data storage bacap_wb_addon:queue current_task{tier:"custom"} run scoreboard players operation #wb_whole wb_math_temp /= #wb_100 wb_math_temp
execute unless data storage bacap_wb_addon:queue current_task{tier:"custom"} run scoreboard players operation #wb_whole wb_math_temp *= #wb_mult wb_math_temp

# Step B: Get the remainder and multiply it (ЗАЩИТА ОТ КАСТОМА)
execute unless data storage bacap_wb_addon:queue current_task{tier:"custom"} run scoreboard players operation #wb_rem wb_math_temp = #wb_base wb_math_temp
execute unless data storage bacap_wb_addon:queue current_task{tier:"custom"} run scoreboard players operation #wb_rem wb_math_temp %= #wb_100 wb_math_temp
execute unless data storage bacap_wb_addon:queue current_task{tier:"custom"} run scoreboard players operation #wb_rem wb_math_temp *= #wb_mult wb_math_temp
execute unless data storage bacap_wb_addon:queue current_task{tier:"custom"} run scoreboard players operation #wb_rem wb_math_temp /= #wb_100 wb_math_temp

# Step C: Combine them back into #wb_base
execute unless data storage bacap_wb_addon:queue current_task{tier:"custom"} run scoreboard players operation #wb_base wb_math_temp = #wb_whole wb_math_temp
execute unless data storage bacap_wb_addon:queue current_task{tier:"custom"} run scoreboard players operation #wb_base wb_math_temp += #wb_rem wb_math_temp

# Save the final size as a double
execute store result storage bacap_wb_addon:macro size double 0.01 run scoreboard players get #wb_base wb_math_temp

# Pass the final number to our format calculator
scoreboard players operation #format_val wb_math_temp = #wb_base wb_math_temp
function bacap_wb_addon:math/format_value

# Copy the ready text pieces into the macro storage for tellraw
data modify storage bacap_wb_addon:macro size_whole set from storage bacap_wb_addon:temp display_format.w
data modify storage bacap_wb_addon:macro size_frac set from storage bacap_wb_addon:temp display_format.f
data modify storage bacap_wb_addon:macro size_pad set from storage bacap_wb_addon:temp display_format.p

# Combine them back into #wb_base
scoreboard players operation #wb_base wb_math_temp = #wb_whole wb_math_temp
scoreboard players operation #wb_base wb_math_temp += #wb_rem wb_math_temp

# Save the final size as a double (for the worldborder command)
# Example: 150 will become 1.5d
execute store result storage bacap_wb_addon:macro size double 0.01 run scoreboard players get #wb_base wb_math_temp

# Pass the final number to our format calculator
scoreboard players operation #format_val wb_math_temp = #wb_base wb_math_temp
function bacap_wb_addon:math/format_value

# Copy the ready text pieces into the macro storage for tellraw
data modify storage bacap_wb_addon:macro size_whole set from storage bacap_wb_addon:temp display_format.w
data modify storage bacap_wb_addon:macro size_frac set from storage bacap_wb_addon:temp display_format.f
data modify storage bacap_wb_addon:macro size_pad set from storage bacap_wb_addon:temp display_format.p
