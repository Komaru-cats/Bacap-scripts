scoreboard objectives add wb dummy
scoreboard objectives add wb_config dummy
scoreboard objectives add wb_adv_blocks dummy
scoreboard objectives add wb_tier_blocks dummy
scoreboard objectives add wb_world_size trigger
scoreboard objectives add wb_math_temp dummy
scoreboard objectives add wb_block_multiplier dummy
scoreboard objectives add wb_base_contrib dummy
scoreboard objectives add wb_real_contrib dummy {"text":"First Advancement Blocks","color":"white"}

# Constants for Newton's formula and conversion to ticks
scoreboard players set #wb_2 wb_math_temp 2
scoreboard players set #wb_4 wb_math_temp 4

# Constant to multiply/divide multiplier
scoreboard players set #wb_40 wb_math_temp 40
scoreboard players set #wb_10 wb_math_temp 10
scoreboard players set #wb_100 wb_math_temp 100
scoreboard players set #wb_1000 wb_math_temp 1000
scoreboard players set #wb_10000 wb_math_temp 10000

execute unless data storage bacap_wb_addon:settings mult_int run data modify storage bacap_wb_addon:settings mult_int set value 100
execute unless data storage bacap_wb_addon:settings multiplier run data modify storage bacap_wb_addon:settings multiplier set value 1.0d


# Check that fast_wb and bossbar settings are not initialized, and if so, we set default settings for them
execute unless score fast_wb wb_config matches 1 unless score fast_wb wb_config matches 0 run scoreboard players set fast_wb wb_config 0
execute unless score bossbar wb_config matches 1 unless score bossbar wb_config matches 0 run scoreboard players set bossbar wb_config 0

# Add 0 to first_time to make it 0, not "null"
scoreboard players add first_time wb 0

# If it matches 0, do install, that works only for the first time
execute if score first_time wb matches 0 run schedule function bacap_wb_addon:system/install 8s

# Set the reward mode
execute unless score reward_mode wb_config matches 0..1 run scoreboard players set reward_mode wb_config 0

# Detect ED scoreboard
scoreboard objectives add wb_is_ed dummy

# Detector
schedule function bacap_wb_addon:detectors/detect_mode 5s