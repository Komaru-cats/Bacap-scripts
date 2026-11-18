tellraw @s {"text":" "}

tellraw @s [{"text":"[ ","color":"dark_gray"},{"translate":"Game Start","color":"yellow","bold":true},{"text":" ]","color":"dark_gray"}]

tellraw @s {"translate":"• The World Border will be reset to 1 block\n• All players will be teleported to the center\n• Current advancements will NOT be reset (progress kept)","color":"#C1C1C1"}

tellraw @s {"text":" "}

tellraw @s [{"text":"[ ","color":"dark_gray"},{"translate":"Confirm & Start","color":"yellow","bold":true,"click_event":{"action":"run_command","command":"/function bacap_wb_addon:config/start_without_advancement_reset"},"hover_event":{"action": "show_text", "value":{"translate":"Start without losing advancements","color":"yellow"}}},{"text":" ]    ","color":"dark_gray"},{"text":"[ ","color":"dark_gray"},{"translate":"Cancel","color":"green","bold":true,"click_event":{"action":"run_command","command":"/function bacap_wb_addon:config"},"hover_event":{"action": "show_text", "value":{"translate":"Safe return to the main menu","color":"green"}}},{"text":" ]","color":"dark_gray"}]