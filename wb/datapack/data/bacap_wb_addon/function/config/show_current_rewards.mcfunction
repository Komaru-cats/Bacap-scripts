# Multiplayer
execute store result score #format_val wb_math_temp run data get storage bacap_wb_addon:settings mult_int 1
function bacap_wb_addon:math/format_value
data modify storage bacap_wb_addon:temp display.mult_w set from storage bacap_wb_addon:temp display_format.w
data modify storage bacap_wb_addon:temp display.mult_f set from storage bacap_wb_addon:temp display_format.f
data modify storage bacap_wb_addon:temp display.mult_p set from storage bacap_wb_addon:temp display_format.p

# Task
scoreboard players operation #format_val wb_math_temp = #task wb_tier_blocks
function bacap_wb_addon:math/format_value
data modify storage bacap_wb_addon:temp display.task_w set from storage bacap_wb_addon:temp display_format.w
data modify storage bacap_wb_addon:temp display.task_f set from storage bacap_wb_addon:temp display_format.f
data modify storage bacap_wb_addon:temp display.task_p set from storage bacap_wb_addon:temp display_format.p

# Goal
scoreboard players operation #format_val wb_math_temp = #goal wb_tier_blocks
function bacap_wb_addon:math/format_value
data modify storage bacap_wb_addon:temp display.goal_w set from storage bacap_wb_addon:temp display_format.w
data modify storage bacap_wb_addon:temp display.goal_f set from storage bacap_wb_addon:temp display_format.f
data modify storage bacap_wb_addon:temp display.goal_p set from storage bacap_wb_addon:temp display_format.p

# Challenge
scoreboard players operation #format_val wb_math_temp = #challenge wb_tier_blocks
function bacap_wb_addon:math/format_value
data modify storage bacap_wb_addon:temp display.chal_w set from storage bacap_wb_addon:temp display_format.w
data modify storage bacap_wb_addon:temp display.chal_f set from storage bacap_wb_addon:temp display_format.f
data modify storage bacap_wb_addon:temp display.chal_p set from storage bacap_wb_addon:temp display_format.p

# Super challenge
scoreboard players operation #format_val wb_math_temp = #super_challenge wb_tier_blocks
function bacap_wb_addon:math/format_value
data modify storage bacap_wb_addon:temp display.schal_w set from storage bacap_wb_addon:temp display_format.w
data modify storage bacap_wb_addon:temp display.schal_f set from storage bacap_wb_addon:temp display_format.f
data modify storage bacap_wb_addon:temp display.schal_p set from storage bacap_wb_addon:temp display_format.p

# Milestone
scoreboard players operation #format_val wb_math_temp = #milestone wb_tier_blocks
function bacap_wb_addon:math/format_value
data modify storage bacap_wb_addon:temp display.mile_w set from storage bacap_wb_addon:temp display_format.w
data modify storage bacap_wb_addon:temp display.mile_f set from storage bacap_wb_addon:temp display_format.f
data modify storage bacap_wb_addon:temp display.mile_p set from storage bacap_wb_addon:temp display_format.p

# Hidden
scoreboard players operation #format_val wb_math_temp = #hidden wb_tier_blocks
function bacap_wb_addon:math/format_value
data modify storage bacap_wb_addon:temp display.hid_w set from storage bacap_wb_addon:temp display_format.w
data modify storage bacap_wb_addon:temp display.hid_f set from storage bacap_wb_addon:temp display_format.f
data modify storage bacap_wb_addon:temp display.hid_p set from storage bacap_wb_addon:temp display_format.p

#
function bacap_wb_addon:ui/config/show_current_rewards_message with storage bacap_wb_addon:temp display