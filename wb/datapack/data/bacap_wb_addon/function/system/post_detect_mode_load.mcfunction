# Init blocks (Order: BACAP -> BACAPED -> Fanpacks)
function bacap_wb_addon:init_blocks/individual/bacap
execute if score bc_wb wb_is_ed matches 1 run function bacap_wb_addon:init_blocks/individual/bacaped
function #bacap_wb_addon:init_blocks

# Init tiers (Strict Order: BACAP -> BACAPED -> Fanpacks)
function bacap_wb_addon:init_blocks/tiers/bacap
execute if score bc_wb wb_is_ed matches 1 run function bacap_wb_addon:init_blocks/tiers/bacaped
function #bacap_wb_addon:init_tiers