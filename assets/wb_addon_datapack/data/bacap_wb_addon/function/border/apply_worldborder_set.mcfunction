$execute in minecraft:overworld run worldborder set $(size) $(time)t
$execute in minecraft:the_nether run worldborder set $(size) $(time)t
$execute in minecraft:the_end run worldborder set $(size) $(time)t

# Bossbar animation
$scoreboard players set wb_bossbar_max wb_math_temp $(time)
scoreboard players set wb_bossbar_timer wb_math_temp 0
execute store result bossbar bacap_wb_addon:world_size max run scoreboard players get wb_bossbar_max wb_math_temp
bossbar set bacap_wb_addon:world_size value 0

$schedule function bacap_wb_addon:system/untask $(time)t