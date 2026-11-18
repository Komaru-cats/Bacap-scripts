function bacap_wb_addon:config

execute run scoreboard objectives remove wb
execute run scoreboard objectives add wb dummy

# Set first time
scoreboard players set first_time wb 1

execute run scoreboard players set is_wb_run wb 1

execute run advancement revoke @a everything
execute run scoreboard objectives remove bac_obtained

execute run scoreboard objectives add bac_obtained dummy

function bacap_wb_addon:start/reset_worldborder_size

function bacap_wb_addon:start/player_tp

scoreboard players set * wb_base_contrib 0
scoreboard players set * wb_custom_contrib 0
scoreboard players set * wb_real_contrib 0

schedule function bacap_wb_addon:start/get_start_kit 8s

execute run function bacap_wb_addon:system/1_second_timer



