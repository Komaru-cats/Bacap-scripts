
# One-time per datapack init (BACAPED OVERRIDE)

# We use a unique initialization flag (#wb_bacap_tiers_init) for the base datapack.
# This guarantees these defaults are applied exactly ONCE. If someone changes
# them via UI later, or if a fanpack overrides them on its own first load,
# a /reload won't revert them back because our flag is already set to 1.
#
# Note: 'ADD' tiers are multiplied by 100 to support decimal places
# (e.g., 1 block = 100, 5.5 blocks = 550, 10 blocks = 1000).

execute unless score #wb_bacaped_tiers_init wb matches 1 run scoreboard players set #task wb_tier_blocks 100
execute unless score #wb_bacaped_tiers_init wb matches 1 run scoreboard players set #goal wb_tier_blocks 400
execute unless score #wb_bacaped_tiers_init wb matches 1 run scoreboard players set #challenge wb_tier_blocks 2000
execute unless score #wb_bacaped_tiers_init wb matches 1 run scoreboard players set #super_challenge wb_tier_blocks 15000
execute unless score #wb_bacaped_tiers_init wb matches 1 run scoreboard players set #milestone wb_tier_blocks 50000
execute unless score #wb_bacaped_tiers_init wb matches 1 run scoreboard players set #hidden wb_tier_blocks 0

# Mark as initialized
execute unless score #wb_bacaped_tiers_init wb matches 1 run scoreboard players set #wb_bacaped_tiers_init wb 1