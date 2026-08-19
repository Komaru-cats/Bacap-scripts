function bacap_wb_addon:config

scoreboard objectives remove wb
scoreboard objectives add wb dummy

scoreboard players set is_wb_run wb 1

function bacap_wb_addon:start/reset_worldborder_size

function bacap_wb_addon:start/player_tp

schedule function bacap_wb_addon:start/get_start_kit 8s

execute run function bacap_wb_addon:system/1_second_timer


