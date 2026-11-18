execute if score is_wb_run wb matches 1 if data storage bacap_wb_addon:queue pending[0] run function bacap_wb_addon:queue/pop_queue

# Bossbar animation
execute if score is_wb_run wb matches 0 run scoreboard players add wb_bossbar_timer wb_math_temp 1
execute if score is_wb_run wb matches 0 store result bossbar bacap_wb_addon:world_size value run scoreboard players get wb_bossbar_timer wb_math_temp