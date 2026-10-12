scoreboard players reset * wb_tier_blocks

scoreboard players reset #wb_bacaped_tiers_init wb
scoreboard players reset #wb_bacap_tiers_init wb

function #bacap_wb_addon:reset_tiers_flags

function bacap_wb_addon:init_blocks/tiers/bacap
execute if score bc_wb wb_is_ed matches 1 run function bacap_wb_addon:init_blocks/tiers/bacaped

function #bacap_wb_addon:init_tiers

tellraw @s {"translate":"Tier rewards have been reset to default values!","color":"green"}