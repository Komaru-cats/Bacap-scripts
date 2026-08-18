tellraw @s {"text":"                                             ","color":"dark_gray","strikethrough":true}
tellraw @s {"text":" "}
tellraw @s {"text":"  How to update to new datapack versions","color":"gold","bold":true}
tellraw @s {"text":" "}

tellraw @s [{"text":" 1) ","color":"yellow"},{"text":"Make a backup of your world for safety if you mess anything up","color":"white"}]
tellraw @s [{"text":" 2) ","color":"yellow"},{"text":"Leave your world for more safety and don't go in during the process","color":"white"}]
tellraw @s [{"text":" 3) ","color":"yellow"},{"text":"Delete the old datapacks COMPLETELY from your world","color":"#FF874B"}]
tellraw @s [{"text":" 4) ","color":"yellow"},{"text":"Copy and paste in the new updated datapacks","color":"white"}]
tellraw @s [{"text":" 5) ","color":"yellow"},{"text":"Go into your world. If the new datapacks are for a newer version of Minecraft make sure you are now using that version","color":"white"}]
tellraw @s [{"text":" 6) ","color":"yellow"},{"text":"If you messed up, go to your backup, make a backup of your backup, then repeat steps 2-6 on the backup","color":"white"}]

tellraw @s {"text":" "}

# Back button
tellraw @s [{"text":"[ ","color":"white","click_event":{"action":"run_command","command":"/function bacap_wb_addon:ui/config/help_menu"},"hover_event":{"action":"show_text","value":{"text":"Return to the Help menu.","color":"gray"}}},{"text":"««","color":"yellow","click_event":{"action":"run_command","command":"/function bacap_wb_addon:ui/config/help_menu"},"hover_event":{"action":"show_text","value":{"text":"Return to the Help menu.","color":"gray"}}},{"text":" ] ","color":"white","click_event":{"action":"run_command","command":"/function bacap_wb_addon:ui/config/help_menu"},"hover_event":{"action":"show_text","value":{"text":"Return to the Help menu.","color":"white"}}},{"text":"Go back to Help Menu","color":"gray","click_event":{"action":"run_command","command":"/function bacap_wb_addon:ui/config/help_menu"},"hover_event":{"action":"show_text","value":{"text":"Return to the Help menu.","color":"gold"}}}]

tellraw @s {"text":"                                             ","color":"dark_gray","strikethrough":true}