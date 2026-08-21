# Block the advancement globally so that the second player cannot activate it.
$scoreboard players set $(adv_id) wb 1

# By default, take the INDIVIDUAL block value from the registry
$scoreboard players operation #current_reward wb_math_temp = $(adv_id) wb_adv_blocks

# TIER OVERRIDE: If tier mode is on (1) AND command is "add", overwrite with tier value
$execute if score reward_mode wb_config matches 1 unless data storage bacap_wb_addon:temp current_adv{tier:"custom"} run scoreboard players operation #current_reward wb_math_temp = #$(tier) wb_tier_blocks

# CUSTOM OVERRIDE (Highest priority)
# Uses the exact value from the advancement pattern NBT
execute if data storage bacap_wb_addon:temp current_adv{tier: "custom"} store result score #current_reward wb_math_temp run data get storage bacap_wb_addon:temp current_adv.custom_tier_blocks

# Save the final calculated blocks into the NBT object
execute store result storage bacap_wb_addon:temp current_adv.blocks int 1 run scoreboard players get #current_reward wb_math_temp

# We give points to the player ONLY if it is the "add" command.
execute if data storage bacap_wb_addon:temp current_adv{type:"add"} unless data storage bacap_wb_addon:temp current_adv{tier:"custom"} run scoreboard players operation @s wb_base_contrib += #current_reward wb_math_temp

execute if data storage bacap_wb_addon:temp current_adv{type:"add"} if data storage bacap_wb_addon:temp current_adv{tier:"custom"} run scoreboard players operation @s wb_custom_contrib += #current_reward wb_math_temp

execute if data storage bacap_wb_addon:temp current_adv{type:"add"} run function bacap_wb_addon:math/recalc_contrib

# Move the finished object to the end of the queue
data modify storage bacap_wb_addon:queue pending append from storage bacap_wb_addon:temp current_adv