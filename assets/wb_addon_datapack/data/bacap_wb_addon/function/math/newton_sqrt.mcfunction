# Input: #wb_sq wb_math_temp (The number to square root)
# Output: #wb_R wb_math_temp (The calculated square root)

# Preparing for Newton (#wb_R = #wb_sq / 2 + 1)
scoreboard players operation #wb_R wb_math_temp = #wb_sq wb_math_temp
scoreboard players operation #wb_R wb_math_temp /= #wb_2 wb_math_temp
scoreboard players add #wb_R wb_math_temp 1

# Newton Iterations (16 times for massive numbers up to 2 billion)
# 1
scoreboard players operation #wb_T wb_math_temp = #wb_sq wb_math_temp
scoreboard players operation #wb_T wb_math_temp /= #wb_R wb_math_temp
scoreboard players operation #wb_R wb_math_temp += #wb_T wb_math_temp
scoreboard players operation #wb_R wb_math_temp /= #wb_2 wb_math_temp
# 2
scoreboard players operation #wb_T wb_math_temp = #wb_sq wb_math_temp
scoreboard players operation #wb_T wb_math_temp /= #wb_R wb_math_temp
scoreboard players operation #wb_R wb_math_temp += #wb_T wb_math_temp
scoreboard players operation #wb_R wb_math_temp /= #wb_2 wb_math_temp
# 3
scoreboard players operation #wb_T wb_math_temp = #wb_sq wb_math_temp
scoreboard players operation #wb_T wb_math_temp /= #wb_R wb_math_temp
scoreboard players operation #wb_R wb_math_temp += #wb_T wb_math_temp
scoreboard players operation #wb_R wb_math_temp /= #wb_2 wb_math_temp
# 4
scoreboard players operation #wb_T wb_math_temp = #wb_sq wb_math_temp
scoreboard players operation #wb_T wb_math_temp /= #wb_R wb_math_temp
scoreboard players operation #wb_R wb_math_temp += #wb_T wb_math_temp
scoreboard players operation #wb_R wb_math_temp /= #wb_2 wb_math_temp
# 5
scoreboard players operation #wb_T wb_math_temp = #wb_sq wb_math_temp
scoreboard players operation #wb_T wb_math_temp /= #wb_R wb_math_temp
scoreboard players operation #wb_R wb_math_temp += #wb_T wb_math_temp
scoreboard players operation #wb_R wb_math_temp /= #wb_2 wb_math_temp
# 6
scoreboard players operation #wb_T wb_math_temp = #wb_sq wb_math_temp
scoreboard players operation #wb_T wb_math_temp /= #wb_R wb_math_temp
scoreboard players operation #wb_R wb_math_temp += #wb_T wb_math_temp
scoreboard players operation #wb_R wb_math_temp /= #wb_2 wb_math_temp
# 7
scoreboard players operation #wb_T wb_math_temp = #wb_sq wb_math_temp
scoreboard players operation #wb_T wb_math_temp /= #wb_R wb_math_temp
scoreboard players operation #wb_R wb_math_temp += #wb_T wb_math_temp
scoreboard players operation #wb_R wb_math_temp /= #wb_2 wb_math_temp
# 8
scoreboard players operation #wb_T wb_math_temp = #wb_sq wb_math_temp
scoreboard players operation #wb_T wb_math_temp /= #wb_R wb_math_temp
scoreboard players operation #wb_R wb_math_temp += #wb_T wb_math_temp
scoreboard players operation #wb_R wb_math_temp /= #wb_2 wb_math_temp
# 9
scoreboard players operation #wb_T wb_math_temp = #wb_sq wb_math_temp
scoreboard players operation #wb_T wb_math_temp /= #wb_R wb_math_temp
scoreboard players operation #wb_R wb_math_temp += #wb_T wb_math_temp
scoreboard players operation #wb_R wb_math_temp /= #wb_2 wb_math_temp
# 10
scoreboard players operation #wb_T wb_math_temp = #wb_sq wb_math_temp
scoreboard players operation #wb_T wb_math_temp /= #wb_R wb_math_temp
scoreboard players operation #wb_R wb_math_temp += #wb_T wb_math_temp
scoreboard players operation #wb_R wb_math_temp /= #wb_2 wb_math_temp
# 11
scoreboard players operation #wb_T wb_math_temp = #wb_sq wb_math_temp
scoreboard players operation #wb_T wb_math_temp /= #wb_R wb_math_temp
scoreboard players operation #wb_R wb_math_temp += #wb_T wb_math_temp
scoreboard players operation #wb_R wb_math_temp /= #wb_2 wb_math_temp
# 12
scoreboard players operation #wb_T wb_math_temp = #wb_sq wb_math_temp
scoreboard players operation #wb_T wb_math_temp /= #wb_R wb_math_temp
scoreboard players operation #wb_R wb_math_temp += #wb_T wb_math_temp
scoreboard players operation #wb_R wb_math_temp /= #wb_2 wb_math_temp
# 13
scoreboard players operation #wb_T wb_math_temp = #wb_sq wb_math_temp
scoreboard players operation #wb_T wb_math_temp /= #wb_R wb_math_temp
scoreboard players operation #wb_R wb_math_temp += #wb_T wb_math_temp
scoreboard players operation #wb_R wb_math_temp /= #wb_2 wb_math_temp
# 14
scoreboard players operation #wb_T wb_math_temp = #wb_sq wb_math_temp
scoreboard players operation #wb_T wb_math_temp /= #wb_R wb_math_temp
scoreboard players operation #wb_R wb_math_temp += #wb_T wb_math_temp
scoreboard players operation #wb_R wb_math_temp /= #wb_2 wb_math_temp
# 15
scoreboard players operation #wb_T wb_math_temp = #wb_sq wb_math_temp
scoreboard players operation #wb_T wb_math_temp /= #wb_R wb_math_temp
scoreboard players operation #wb_R wb_math_temp += #wb_T wb_math_temp
scoreboard players operation #wb_R wb_math_temp /= #wb_2 wb_math_temp
# 16
scoreboard players operation #wb_T wb_math_temp = #wb_sq wb_math_temp
scoreboard players operation #wb_T wb_math_temp /= #wb_R wb_math_temp
scoreboard players operation #wb_R wb_math_temp += #wb_T wb_math_temp
scoreboard players operation #wb_R wb_math_temp /= #wb_2 wb_math_temp