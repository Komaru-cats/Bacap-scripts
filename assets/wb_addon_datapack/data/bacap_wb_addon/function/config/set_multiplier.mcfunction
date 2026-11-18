# Attempt to save the input. If the player entered text instead of numbers, the NBT modification fails and success will be 0.
$execute store success score #valid_input wb_math_temp run data modify storage bacap_wb_addon:temp check_val set value $(value)d

# If the input is invalid (letters or empty), send an error message and HALT execution.
execute store success score #valid_input wb_math_temp store result score #wb_check_mult wb_math_temp run data get storage bacap_wb_addon:temp check_val 10
execute if score #valid_input wb_math_temp matches 0 run tellraw @s [{"translate":"Invalid input! Please enter a valid number (e.g., 1.5).","color":"red"}]
execute if score #valid_input wb_math_temp matches 0 run return 0

# Extract the value with rounding to fix floating point precision issues (since we reached here, the input is definitely a number).
execute store result score #wb_check_mult wb_math_temp run data get storage bacap_wb_addon:temp check_val 100000
scoreboard players add #wb_check_mult wb_math_temp 500
scoreboard players operation #wb_check_mult wb_math_temp /= #wb_1000 wb_math_temp

# Check if the value is too low (<= 0.79). Includes 0 and negative numbers.
execute if score #wb_check_mult wb_math_temp matches ..79 run tellraw @s [{"translate":"This multiplier is too low! The game will be impossible to complete. Please use 0.8 or higher.","color":"#FFC162"}]
execute if score #wb_check_mult wb_math_temp matches ..79 run return 0

# Check if the value is too high (>= 10.01).
execute if score #wb_check_mult wb_math_temp matches 1001.. run tellraw @s [{"translate":"This multiplier is too high! It may cause overflows during calculations. Please use 10 or lower.","color":"#FFC162"}]
execute if score #wb_check_mult wb_math_temp matches 1001.. run return 0

# If the script reached this line, it means the input value is PERFECT.
# We no longer need to write 'matches 80..1000' on every line, we just apply it!

# Save the multiplier to the settings storage
$data modify storage bacap_wb_addon:settings multiplier set value $(value)d
execute store result storage bacap_wb_addon:settings mult_int int 1 run scoreboard players get #wb_check_mult wb_math_temp
tellraw @s [{"translate":"The multiplier has been successfully updated!","color":"green"}]

# Prepare data and save the change to history
execute store result storage bacap_wb_addon:temp gametime int 1 run time query gametime
# Create a history object specifically for the multiplier
$data modify storage bacap_wb_addon:temp history_data set value {type: "multiplier", value: $(value)d}
function bacap_wb_addon:system/save_history with storage bacap_wb_addon:temp

# Recalculate the real contribution for ALL online players
execute as @a run function bacap_wb_addon:math/recalc_contrib