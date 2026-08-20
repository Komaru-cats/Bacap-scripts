# MARK THAT ADVANCEMENT PROCESS STARTED
scoreboard players set is_wb_run wb 0

# Copy current task to a temporary object to avoid NBT array syntax errors
data modify storage bacap_wb_addon:queue current_task set from storage bacap_wb_addon:queue pending[0]

# ZERO-BLOCK case (Hidden by default, Roots)
# If the reward is 0 blocks, instantly release the queue and abort the script!
# This prevents the "+0.00 Blocks" message and saves CPU from running math.
execute if data storage bacap_wb_addon:queue current_task{blocks: 0} run function bacap_wb_addon:system/untask
execute if data storage bacap_wb_addon:queue current_task{blocks: 0} run return 0

# Save the text data in the same bacap_wb_addon:macro storage where size and time are already stored.
$data modify storage bacap_wb_addon:macro adv_title set value "$(title)"
$data modify storage bacap_wb_addon:macro adv_title_color set value "$(title_color)"
$data modify storage bacap_wb_addon:macro adv_desc set value "$(desc)"
$data modify storage bacap_wb_addon:macro adv_desc_color set value "$(desc_color)"
$data modify storage bacap_wb_addon:macro adv_tab set value "$(tab)"

# Apply barrier expansion (type: add)
$execute if data storage bacap_wb_addon:queue current_task{type:"add"} if score fast_wb wb_config matches 0 run function bacap_wb_addon:math/border_calculator {blocks: $(blocks)}
$execute if data storage bacap_wb_addon:queue current_task{type:"add"} if score fast_wb wb_config matches 1 run function bacap_wb_addon:math/border_calculator_fast {blocks: $(blocks)}
execute if data storage bacap_wb_addon:queue current_task{type:"add"} if score fast_wb wb_config matches 0 run function bacap_wb_addon:border/apply_worldborder with storage bacap_wb_addon:macro
execute if data storage bacap_wb_addon:queue current_task{type:"add"} if score fast_wb wb_config matches 1 run function bacap_wb_addon:border/apply_worldborder_fast with storage bacap_wb_addon:macro

# Apply barrier expansion (type: set)
$execute if data storage bacap_wb_addon:queue current_task{type:"set"} if score fast_wb wb_config matches 0 run function bacap_wb_addon:math/border_calculator_set {target_blocks: $(blocks)}
$execute if data storage bacap_wb_addon:queue current_task{type:"set"} if score fast_wb wb_config matches 1 run function bacap_wb_addon:math/border_calculator_set_fast {target_blocks: $(blocks)}
execute if data storage bacap_wb_addon:queue current_task{type:"set"} if score fast_wb wb_config matches 0 run function bacap_wb_addon:border/apply_worldborder_set with storage bacap_wb_addon:macro
execute if data storage bacap_wb_addon:queue current_task{type:"set"} if score fast_wb wb_config matches 1 run function bacap_wb_addon:border/apply_worldborder_set_fast with storage bacap_wb_addon:macro

# MESSAGE ROUTING
execute unless data storage bacap_wb_addon:queue current_task{tier:"custom"} run function bacap_wb_addon:ui/send_message with storage bacap_wb_addon:macro

execute if data storage bacap_wb_addon:queue current_task{tier:"custom"} run function bacap_wb_addon:ui/send_message_custom_tier_blocks with storage bacap_wb_addon:macro