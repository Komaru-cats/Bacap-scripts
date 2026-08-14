# 0. Block the advancement globally so that the second player cannot activate it.
$scoreboard players set $(adv_id) wb 1

# 1. By default, take the INDIVIDUAL block value from the registry
$scoreboard players operation #current_reward wb_math_temp = $(adv_id) wb_adv_blocks

# 2. TIER OVERRIDE: If tier mode is on (1) AND command is "add", overwrite with tier value
# (The macro will dynamically turn #$(tier) into #task, #goal, etc.)
$execute if score reward_mode wb_config matches 1 run scoreboard players operation #current_reward wb_math_temp = #$(tier) wb_tier_blocks

# 3. Save the final calculated blocks into the NBT object
execute store result storage bacap_wb_addon:temp current_adv.blocks int 1 run scoreboard players get #current_reward wb_math_temp

# 4. We give points to the player ONLY if it is the "add" command.
execute if data storage bacap_wb_addon:temp current_adv{type:"add"} run scoreboard players operation @s wb_base_contrib += #current_reward wb_math_temp
execute if data storage bacap_wb_addon:temp current_adv{type:"add"} run function bacap_wb_addon:math/recalc_contrib

# 5. Move the finished object to the end of the queue
data modify storage bacap_wb_addon:queue pending append from storage bacap_wb_addon:temp current_adv