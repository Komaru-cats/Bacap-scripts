# 1. Capture the passed number in a temporary variable #wb_base
$scoreboard players set #wb_base wb_math_temp $(blocks)

# 2. Applying a multiplier
execute store result score #wb_mult wb_math_temp run data get storage bacap_wb_addon:settings mult_int 1

# Step A: Get the whole part and multiply it
# #wb_whole = (#wb_base / 100) * #wb_mult
scoreboard players operation #wb_whole wb_math_temp = #wb_base wb_math_temp
scoreboard players operation #wb_whole wb_math_temp /= #wb_100 wb_math_temp
scoreboard players operation #wb_whole wb_math_temp *= #wb_mult wb_math_temp

# Step B: Get the remainder and multiply it
# #wb_rem = ((#wb_base % 100) * #wb_mult) / 100
scoreboard players operation #wb_rem wb_math_temp = #wb_base wb_math_temp
scoreboard players operation #wb_rem wb_math_temp %= #wb_100 wb_math_temp
scoreboard players operation #wb_rem wb_math_temp *= #wb_mult wb_math_temp
scoreboard players operation #wb_rem wb_math_temp /= #wb_100 wb_math_temp

# Step C: Combine them back into #wb_base
scoreboard players operation #wb_base wb_math_temp = #wb_whole wb_math_temp
scoreboard players operation #wb_base wb_math_temp += #wb_rem wb_math_temp

# 3. Save the final size as a fraction
execute store result storage bacap_wb_addon:macro size double 0.01 run scoreboard players get #wb_base wb_math_temp

# Integer part
scoreboard players operation #wb_whole wb_math_temp = #wb_base wb_math_temp
scoreboard players operation #wb_whole wb_math_temp /= #wb_100 wb_math_temp

# Fractional part
scoreboard players operation #wb_frac wb_math_temp = #wb_base wb_math_temp
scoreboard players operation #wb_frac wb_math_temp %= #wb_100 wb_math_temp

# Send them to the macro storage
execute store result storage bacap_wb_addon:macro size_whole int 1 run scoreboard players get #wb_whole wb_math_temp
execute store result storage bacap_wb_addon:macro size_frac int 1 run scoreboard players get #wb_frac wb_math_temp

# Protection against zero loss
execute if score #wb_frac wb_math_temp matches 0..9 run data modify storage bacap_wb_addon:macro size_pad set value "0"
execute if score #wb_frac wb_math_temp matches 10..99 run data modify storage bacap_wb_addon:macro size_pad set value ""

# 4. Preparing for Newton
scoreboard players operation #wb_sq wb_math_temp = #wb_base wb_math_temp
function bacap_wb_addon:math/newton_sqrt

# 5. We get ticks (Root * 4 + 1)
scoreboard players operation #wb_R wb_math_temp *= #wb_4 wb_math_temp
scoreboard players add #wb_R wb_math_temp 1

# 6. Save time in NBT
execute store result storage bacap_wb_addon:macro time int 1 run scoreboard players get #wb_R wb_math_temp