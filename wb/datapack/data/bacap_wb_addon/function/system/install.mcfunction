# This scoreboard check locks the expansion process (creates pseudo-queue)
scoreboard players set is_wb_run wb 1

# We set worldborder in all dimensions to 1 block
execute in minecraft:overworld run worldborder center 0.5 0.5
execute in minecraft:overworld run worldborder set 1
execute in minecraft:overworld run worldborder damage buffer 1
execute in minecraft:overworld run worldborder damage amount 5
execute in minecraft:the_nether run worldborder center 0.5 0.5
execute in minecraft:the_nether run worldborder set 1
execute in minecraft:the_nether run worldborder damage buffer 1
execute in minecraft:the_nether run worldborder damage amount 5
execute in minecraft:the_end run worldborder center 0.5 0.5
execute in minecraft:the_end run worldborder set 1
execute in minecraft:the_end run worldborder damage buffer 1
execute in minecraft:the_end run worldborder damage amount 5

# Teleport all players to the center
function bacap_wb_addon:start/player_tp

# Barrel with start kit
schedule function bacap_wb_addon:start/get_start_kit 8s

# Enable coop mode
function blazeandcave:config/coop_on

# We run config
execute as @a run function bacap_wb_addon:config

scoreboard objectives add wb_first dummy
scoreboard players set wb_global_1 wb_first 0

# Check that BACAP is installed
schedule function bacap_wb_addon:start/wb_addon_not_installed 1s
execute if score bac_created bac_created matches 1 run schedule clear bacap_wb_addon:start/wb_addon_not_installed

# Default bossbar settings
bossbar add bacap_wb_addon:world_size ""
bossbar set bacap_wb_addon:world_size visible false
bossbar set bacap_wb_addon:world_size color blue
bossbar set bacap_wb_addon:world_size max 1
bossbar set bacap_wb_addon:world_size value 1
bossbar set bacap_wb_addon:world_size players @a

scoreboard players set first_time wb 1

function bacap_wb_addon:system/1_second_timer