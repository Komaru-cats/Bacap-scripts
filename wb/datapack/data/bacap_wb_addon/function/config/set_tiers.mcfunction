# Store the user inputs into a temporary NBT object (as doubles)
$data modify storage bacap_wb_addon:temp ui_tiers set value {task: $(task)d, goal: $(goal)d, challenge: $(challenge)d, super_challenge: $(super_challenge)d, milestone: $(milestone)d, hidden: $(hidden)d}

# Assume inputs are valid by default (1 = valid, 0 = invalid)
scoreboard players set #is_valid wb_math_temp 1

# Validate Upper Limits
# (Raw value must be <= 21,474,836 to avoid *100 overflow in the scoreboard)
execute store result score #val wb_math_temp run data get storage bacap_wb_addon:temp ui_tiers.task 1
execute if score #val wb_math_temp matches 21474837.. run scoreboard players set #is_valid wb_math_temp 0
execute store result score #val wb_math_temp run data get storage bacap_wb_addon:temp ui_tiers.goal 1
execute if score #val wb_math_temp matches 21474837.. run scoreboard players set #is_valid wb_math_temp 0
execute store result score #val wb_math_temp run data get storage bacap_wb_addon:temp ui_tiers.challenge 1
execute if score #val wb_math_temp matches 21474837.. run scoreboard players set #is_valid wb_math_temp 0
execute store result score #val wb_math_temp run data get storage bacap_wb_addon:temp ui_tiers.super_challenge 1
execute if score #val wb_math_temp matches 21474837.. run scoreboard players set #is_valid wb_math_temp 0
execute store result score #val wb_math_temp run data get storage bacap_wb_addon:temp ui_tiers.milestone 1
execute if score #val wb_math_temp matches 21474837.. run scoreboard players set #is_valid wb_math_temp 0
execute store result score #val wb_math_temp run data get storage bacap_wb_addon:temp ui_tiers.hidden 1
execute if score #val wb_math_temp matches 21474837.. run scoreboard players set #is_valid wb_math_temp 0

# Validate Lower Limits
# (Scaled value must be >= 1. If it's <= 0, it's invalid UNLESS it is strictly 0.0)
execute store result score #val wb_math_temp run data get storage bacap_wb_addon:temp ui_tiers.task 100
execute if score #val wb_math_temp matches ..0 unless data storage bacap_wb_addon:temp {ui_tiers:{task:0.0d}} run scoreboard players set #is_valid wb_math_temp 0
execute store result score #val wb_math_temp run data get storage bacap_wb_addon:temp ui_tiers.goal 100
execute if score #val wb_math_temp matches ..0 unless data storage bacap_wb_addon:temp {ui_tiers:{goal:0.0d}} run scoreboard players set #is_valid wb_math_temp 0
execute store result score #val wb_math_temp run data get storage bacap_wb_addon:temp ui_tiers.challenge 100
execute if score #val wb_math_temp matches ..0 unless data storage bacap_wb_addon:temp {ui_tiers:{challenge:0.0d}} run scoreboard players set #is_valid wb_math_temp 0
execute store result score #val wb_math_temp run data get storage bacap_wb_addon:temp ui_tiers.super_challenge 100
execute if score #val wb_math_temp matches ..0 unless data storage bacap_wb_addon:temp {ui_tiers:{super_challenge:0.0d}} run scoreboard players set #is_valid wb_math_temp 0
execute store result score #val wb_math_temp run data get storage bacap_wb_addon:temp ui_tiers.milestone 100
execute if score #val wb_math_temp matches ..0 unless data storage bacap_wb_addon:temp {ui_tiers:{milestone:0.0d}} run scoreboard players set #is_valid wb_math_temp 0
execute store result score #val wb_math_temp run data get storage bacap_wb_addon:temp ui_tiers.hidden 100
execute if score #val wb_math_temp matches ..0 unless data storage bacap_wb_addon:temp {ui_tiers:{hidden:0.0d}} run scoreboard players set #is_valid wb_math_temp 0
# Handle Invalid Input (Abort everything)
execute if score #is_valid wb_math_temp matches 0 run tellraw @s {"text": "All tier values must be between 0.01 and 21,474,836 (or exactly 0)! Changes cancelled.", "color": "red"}
execute if score #is_valid wb_math_temp matches 0 run return 0


# Handle Invalid Input (Abort everything)
execute if score #is_valid wb_math_temp matches 0 run tellraw @s {"text": "All tier values must be between 0.01 and 21,474,836! Changes cancelled.", "color": "red"}
execute if score #is_valid wb_math_temp matches 0 run return 0

# Apply Valid Inputs to the Scoreboards (Scale by 100)
execute store result score #task wb_tier_blocks run data get storage bacap_wb_addon:temp ui_tiers.task 100
execute store result score #goal wb_tier_blocks run data get storage bacap_wb_addon:temp ui_tiers.goal 100
execute store result score #challenge wb_tier_blocks run data get storage bacap_wb_addon:temp ui_tiers.challenge 100
execute store result score #super_challenge wb_tier_blocks run data get storage bacap_wb_addon:temp ui_tiers.super_challenge 100
execute store result score #milestone wb_tier_blocks run data get storage bacap_wb_addon:temp ui_tiers.milestone 100
execute store result score #hidden wb_tier_blocks run data get storage bacap_wb_addon:temp ui_tiers.hidden 100

# Prepare and Save History Data
execute store result storage bacap_wb_addon:temp gametime int 1 run time query gametime
# Initialize the history object with the type
data modify storage bacap_wb_addon:temp history_data set value {type: "tiers"}
# Merge all user inputs directly into our history object
data modify storage bacap_wb_addon:temp history_data merge from storage bacap_wb_addon:temp ui_tiers
function bacap_wb_addon:system/save_history with storage bacap_wb_addon:temp

# Success Message
tellraw @s {"translate": "Tier rewards successfully updated!", "color": "green"}