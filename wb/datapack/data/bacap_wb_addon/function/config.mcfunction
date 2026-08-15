tellraw @s {"text":"                                             ","color":"dark_gray","strikethrough":true}

# Start button (Keep Advancements)
tellraw @s [{"text":"[ "},{"text":"▶","color":"#6DFF9C"},{"text":" ] "},{"translate":"Start (Keep Advancements)","color":"#6DFF9C","click_event":{"action":"run_command","command":"/function bacap_wb_addon:config/start_without_advancement_reset_message"},"hover_event":{"action": "show_text", "value":{"translate":"Start the game.\nThe World border resets to 1 block and all players are teleported!","color":"gold"}}}]

# Start button (Reset Advancements)
tellraw @s [{"text":"[ "},{"text":"☄","color":"#FF874B"},{"text":" ] "},{"translate":"Start (Reset Advancements)","color":"#FF874B","click_event":{"action":"run_command","command":"/function bacap_wb_addon:config/start_with_advancement_reset_message"},"hover_event":{"action": "show_text", "value":{"translate":"This will remove ALL advancements from all players!\nThe World border resets to 1 block and all players are teleported!","color":"gold"}}}]

tellraw @s {"text": ""}

# Global Multiplier Configuration
tellraw @s [{"text":"[ "},{"text":"×","color":"green"},{"text":" ] "},{"translate":"Configure Global Multiplier","color":"#8CD8FF","click_event":{"action":"run_command","command":"/dialog show @s bacap_wb_addon:config/set_multiplier"},"hover_event":{"action": "show_text", "value":{"translate":"Specify the global multiplier for the blocks granted upon advancement completion.","color":"gold"}}}]

# Tier Blocks Configuration
tellraw @s [{"text":"[ "},{"text":"❖","color":"aqua"},{"text":" ] "},{"translate":"Configure Tier Rewards","color":"#8CD8FF","click_event":{"action":"run_command","command":"/dialog show @s bacap_wb_addon:config/set_tiers"},"hover_event":{"action": "show_text", "value":{"translate":"Set fixed block rewards for tasks, goals, challenges, etc.","color":"gold"}}}]

# Reset Tiers
tellraw @s [{"text":"[ "},{"text":"🔥","color":"#FF874B"},{"text":" ] "},{"translate":"Reset Tier Rewards to Default","color":"#8CD8FF","click_event":{"action":"run_command","command":"/function bacap_wb_addon:config/reset_tiers_to_default_message"},"hover_event":{"action": "show_text", "value":{"translate":"Reset all tier block values to default.","color":"gold"}}}]

tellraw @s {"text": ""}

# Reward Mode Toggle (Individual vs Fixed Tiers)
execute if score reward_mode wb_config matches 0 run tellraw @s [{"text":"[ "},{"text":"📝","color":"#00FFFF"},{"text":" ] "},{"translate":"Reward Mode: Individual Blocks","color":"#FFCBE7","click_event":{"action":"run_command","command":"/function bacap_wb_addon:config/settings/reward_mode_tiers"},"hover_event":{"action": "show_text", "value":{"translate":"Click to switch to Tier-based rewards.\nCurrently: Each advancement gives a specific number of blocks.","color":"gold"}}}]
execute if score reward_mode wb_config matches 1 run tellraw @s [{"text":"[ "},{"text":"📊","color":"#00FFFF"},{"text":" ] "},{"translate":"Reward Mode: Fixed Tiers","color":"#FFCBE7","click_event":{"action":"run_command","command":"/function bacap_wb_addon:config/settings/reward_mode_individual"},"hover_event":{"action": "show_text", "value":{"translate":"Click to switch to Individual-based rewards.\nCurrently: Advancements give a fixed amount based on their tier.","color":"gold"}}}]

# Barrier Expansion Mode Toggle (Fast / Normal)
execute if score fast_wb wb_config matches 0 run tellraw @s [{"text":"[ "},{"text":"⚡","color":"yellow"},{"text":" ] "},{"translate":"Enable Fast Mode","color":"#FFCBE7","click_event":{"action":"run_command","command":"/function bacap_wb_addon:config/settings/fast_mode"},"hover_event":{"action": "show_text", "value":{"translate":"In this mode, the world border will increase instantly.","color":"gold"}}}]
execute if score fast_wb wb_config matches 1 run tellraw @s [{"text":"[ "},{"text":"⌚","color":"green"},{"text":" ] "},{"translate":"Enable Smooth Mode","color":"#FFCBE7","click_event":{"action":"run_command","command":"/function bacap_wb_addon:config/settings/normal_mode"},"hover_event":{"action": "show_text", "value":{"translate":"In this mode, the world border will increase gradually over a few seconds.","color":"gold"}}}]

# Bossbar Toggle (On / Off)
execute if score bossbar wb_config matches 0 run tellraw @s [{"text":"[ "},{"text":"⏻","color":"red"},{"text":" ] "},{"translate":"Show Radius Bossbar","color":"#FFCBE7","click_event":{"action":"run_command","command":"/function bacap_wb_addon:config/settings/bossbar_on"},"hover_event":{"action": "show_text", "value":{"translate":"Display a bossbar at the top of the screen showing the current world radius.","color":"gold"}}}]
execute if score bossbar wb_config matches 1 run tellraw @s [{"text":"[ "},{"text":"⏻","color":"green"},{"text":" ] "},{"translate":"Hide Radius Bossbar","color":"#FFCBE7","click_event":{"action":"run_command","command":"/function bacap_wb_addon:config/settings/bossbar_off"},"hover_event":{"action": "show_text", "value":{"translate":"Hide the world border radius bossbar for all players.","color":"gold"}}}]

tellraw @s [{"translate":"Tip: Players can check the World Size anytime using /trigger wb_world_size","color":"#C1C1C1","italic":true}]

function bacap_wb_addon:config/version

