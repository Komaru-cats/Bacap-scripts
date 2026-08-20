execute store result storage bacap_wb_addon:world_size world.size int 0.5 run worldborder get
bossbar set bacap_wb_addon:world_size name {"translate":"World Size: %1$s blocks","with":[{"nbt":"world.size","storage":"bacap_wb_addon:world_size"}]}

scoreboard players enable @a wb_world_size
execute as @a if score @s wb_world_size matches 1.. run function bacap_wb_addon:ui/world_size_trigger
bossbar set bacap_wb_addon:world_size players @a

schedule function bacap_wb_addon:system/1_second_timer 1s
