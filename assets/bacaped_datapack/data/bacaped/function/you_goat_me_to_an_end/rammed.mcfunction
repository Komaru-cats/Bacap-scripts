# Record world gametime on goat ram if the player is still eligible
execute if entity @s[gamemode=!spectator,advancements={bacaped:end/you_goat_me_to_an_end=false}] store result score @s bacaped_you_goat_me_to_an_end_timer run time query gametime
advancement revoke @s only bacaped:technical/you_goat_me_to_an_end_ram
