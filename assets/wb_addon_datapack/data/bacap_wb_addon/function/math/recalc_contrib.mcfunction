# Take the multiplier (e.g. 1.0 -> 100, 10.0 -> 1000)
execute store result score #wb_mult wb_math_temp run data get storage bacap_wb_addon:settings mult_int 1

# Step A: The whole part
scoreboard players operation #wb_whole wb_math_temp = @s wb_base_contrib
scoreboard players operation #wb_whole wb_math_temp /= #wb_10000 wb_math_temp
scoreboard players operation #wb_whole wb_math_temp *= #wb_mult wb_math_temp

# Step B: The remainder part
scoreboard players operation #wb_rem wb_math_temp = @s wb_base_contrib
scoreboard players operation #wb_rem wb_math_temp %= #wb_10000 wb_math_temp
scoreboard players operation #wb_rem wb_math_temp *= #wb_mult wb_math_temp
scoreboard players operation #wb_rem wb_math_temp /= #wb_10000 wb_math_temp

# Step C: Combine
scoreboard players operation #wb_final wb_math_temp = #wb_whole wb_math_temp
scoreboard players operation #wb_final wb_math_temp += #wb_rem wb_math_temp

# Since wb_custom_contrib is multiplied by 100 (to account for hundredths),
# and the table (wb_real_contrib) stores whole numbers, we divide the value by 100 before adding it,
# so that the player receives exactly 70,000 instead of 7,000,000.
scoreboard players operation #custom_display wb_math_temp = @s wb_custom_contrib
scoreboard players operation #custom_display wb_math_temp /= #wb_100 wb_math_temp
scoreboard players operation #wb_final wb_math_temp += #custom_display wb_math_temp

# Assign to the display scoreboard
scoreboard players operation @s wb_real_contrib = #wb_final wb_math_temp