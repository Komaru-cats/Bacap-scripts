tellraw @s {"text":" "}

tellraw @s [{"text":"[ ","color":"dark_gray"},{"translate":"Game Start Without Advancements","color":"yellow","bold":true},{"text":" ]","color":"dark_gray"}]

tellraw @s {"translate":"• All advancements will be revoked for everyone\n• The World Border will be reset to 1 block\n• All players will be teleported to the center","color":"#C1C1C1"}

tellraw @s {"text":" "}

tellraw @s [{"text":"[ ","color":"dark_gray"},{"translate":"Confirm & Start","color":"red","bold":true,"click_event":{"action":"run_command","command":"/function bacap_wb_addon:config/start_with_advancement_reset"},"hover_event":{"action": "show_text", "value":{"translate":"Wipe progress and start!","color":"red"}}},{"text":" ]","color":"dark_gray"},{"text":"[ ","color":"dark_gray"},{"translate":"Cancel","color":"green","bold":true,"click_event":{"action":"run_command","command":"/function bacap_wb_addon:config"},"hover_event":{"action": "show_text", "value":{"translate":"Safe return to the main menu","color":"green"}}},{"text":" ]","color":"dark_gray"}]
