tellraw @s {"text":" "}

tellraw @s [{"text":"[ ","color":"dark_gray"},{"translate":"Reset Tier Rewards","color":"yellow","bold":true},{"text":" ]","color":"dark_gray"}]

tellraw @s {"translate":"• All tier blocks will be reset to their default values\n• Any custom manual settings will be lost\n• Addon/Fanpack defaults will be safely reapplied","color":"#C1C1C1"}

tellraw @s {"text":" "}

tellraw @s [{"text":"[ ","color":"dark_gray"},{"translate":"Confirm & Reset","color":"yellow","bold":true,"click_event":{"action":"run_command","command":"/function bacap_wb_addon:config/reset_tiers_to_default"},"hover_event":{"action": "show_text", "value":{"translate":"Reset to default values","color":"yellow"}}},{"text":" ]    ","color":"dark_gray"},{"text":"[ ","color":"dark_gray"},{"translate":"Cancel","color":"green","bold":true,"click_event":{"action":"run_command","command":"/function bacap_wb_addon:config"},"hover_event":{"action": "show_text", "value":{"translate":"Safe return to the main menu","color":"green"}}},{"text":" ]","color":"dark_gray"}]