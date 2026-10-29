# Painting facing South (+Z) -> passage is behind it (-Z)
execute at @e[type=painting,distance=..3.5,y_rotation=-45..45,limit=1] positioned ~-2.5 ~-2.5 ~-0.4 if entity @s[dx=5,dy=5,dz=0.1] run advancement grant @s only bacaped:building/secret_passage

# Painting facing West (-X) -> passage is behind it (+X)
execute at @e[type=painting,distance=..3.5,y_rotation=45..135,limit=1] positioned ~0.1 ~-2.5 ~-2.5 if entity @s[dx=0.1,dy=5,dz=5] run advancement grant @s only bacaped:building/secret_passage

# Painting facing East (+X) -> passage is behind it (-X)
execute at @e[type=painting,distance=..3.5,y_rotation=-135..-45,limit=1] positioned ~-0.4 ~-2.5 ~-2.5 if entity @s[dx=0.1,dy=5,dz=5] run advancement grant @s only bacaped:building/secret_passage

# Painting facing North (-Z) -> passage is behind it (+Z)
execute at @e[type=painting,distance=..3.5,y_rotation=135..180,limit=1] positioned ~-2.5 ~-2.5 ~0.1 if entity @s[dx=5,dy=5,dz=0.1] run advancement grant @s only bacaped:building/secret_passage

execute at @e[type=painting,distance=..3.5,y_rotation=-180..-135,limit=1] positioned ~-2.5 ~-2.5 ~0.1 if entity @s[dx=5,dy=5,dz=0.1] run advancement grant @s only bacaped:building/secret_passage
