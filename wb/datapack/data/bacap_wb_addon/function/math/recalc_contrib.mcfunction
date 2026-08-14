# 1. Take the multiplier (e.g. 1.0 -> 100, 10.0 -> 1000)
execute store result score #wb_mult wb_math_temp run data get storage bacap_wb_addon:settings mult_int 1

# We need to calculate: (wb_base_contrib * mult_int) / 10000
# We split it into two parts using 10000 to NEVER exceed 2.14B.

# Step A: The whole part
scoreboard players operation #wb_whole wb_math_temp = @s wb_base_contrib
scoreboard players operation #wb_whole wb_math_temp /= #wb_10000 wb_math_temp
scoreboard players operation #wb_whole wb_math_temp *= #wb_mult wb_math_temp

# Step B: The remainder part
scoreboard players operation #wb_rem wb_math_temp = @s wb_base_contrib
scoreboard players operation #wb_rem wb_math_temp %= #wb_10000 wb_math_temp
scoreboard players operation #wb_rem wb_math_temp *= #wb_mult wb_math_temp
scoreboard players operation #wb_rem wb_math_temp /= #wb_10000 wb_math_temp

# Step C: Combine and output to display
scoreboard players operation #wb_final wb_math_temp = #wb_whole wb_math_temp
scoreboard players operation #wb_final wb_math_temp += #wb_rem wb_math_temp

# Assign to the display scoreboard
scoreboard players operation @s wb_real_contrib = #wb_final wb_math_temp