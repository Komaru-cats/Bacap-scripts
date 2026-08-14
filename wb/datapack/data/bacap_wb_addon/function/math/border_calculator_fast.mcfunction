# 1. Capture the passed number (for example, 30) in a temporary variable #wb_base
$scoreboard players set #wb_base wb_math_temp $(blocks)

# 2. Applying a multiplier

# Read the pre-calculated integer multiplier from NBT (No precision loss!)
execute store result score #wb_mult wb_math_temp run data get storage bacap_wb_addon:settings mult_int 1

# Multiply our blocks by this factor
scoreboard players operation #wb_base wb_math_temp *= #wb_mult wb_math_temp

# Divide it by 100 to return to the original format
scoreboard players operation #wb_base wb_math_temp /= #wb_100 wb_math_temp

# 3. Save the final size as a fraction (temporarily put it in NBT for the final macro)
# 150 will become 1.5
execute store result storage bacap_wb_addon:macro size double 0.01 run scoreboard players get #wb_base wb_math_temp