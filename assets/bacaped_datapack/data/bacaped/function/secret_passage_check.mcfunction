# Secret Passage Hitbox Intersection Check
# Tests each nearby painting directly via @s[dx/dy/dz] to verify overlap with the player's inner core:
# [player_x-0.2..player_x+0.2, player_y+0.2..player_y+1.4, player_z-0.2..player_z+0.2].

execute as @e[type=minecraft:painting,distance=..4] positioned ~-0.2 ~0.2 ~-0.2 if entity @s[dx=0,dy=0.2,dz=0] positioned ~-0.6 ~ ~-0.6 if entity @s[dx=0,dy=0.2,dz=0] run return 1
return fail
