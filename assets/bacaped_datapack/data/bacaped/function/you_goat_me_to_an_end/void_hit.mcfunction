advancement revoke @s only bacaped:technical/you_goat_me_to_an_end_void_death

# Exit early before reading player NBT if there is no active timestamp or the player is ineligible
execute unless entity @s[gamemode=!spectator,advancements={bacaped:end/you_goat_me_to_an_end=false},scores={bacaped_you_goat_me_to_an_end_timer=1..}] run return 0
execute unless entity @s[nbt={Health:0.0f}] run return 0

# Check whether death occurred within 150 ticks (7.5s) after the goat ram
execute store result score #diff bacaped_temp run time query gametime
scoreboard players operation #diff bacaped_temp -= @s bacaped_you_goat_me_to_an_end_timer

execute if score #diff bacaped_temp matches 0..150 run advancement grant @s only bacaped:end/you_goat_me_to_an_end
scoreboard players reset @s bacaped_you_goat_me_to_an_end_timer
