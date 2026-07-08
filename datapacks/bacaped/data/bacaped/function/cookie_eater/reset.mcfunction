execute store result score current_day bacaped_current_day run time query day
execute as @a unless score @s bacaped_current_day = current_day bacaped_current_day run scoreboard players set @s bacaped_cookies_eaten_today 0
execute as @a unless score @s bacaped_current_day = current_day bacaped_current_day run scoreboard players operation @s bacaped_current_day = current_day bacaped_current_day