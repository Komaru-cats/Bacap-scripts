scoreboard players operation #format_whole wb_math_temp = #format_val wb_math_temp
scoreboard players operation #format_whole wb_math_temp /= #wb_100 wb_math_temp

scoreboard players operation #format_frac wb_math_temp = #format_val wb_math_temp
scoreboard players operation #format_frac wb_math_temp %= #wb_100 wb_math_temp

execute store result storage bacap_wb_addon:temp display_format.w int 1 run scoreboard players get #format_whole wb_math_temp
execute store result storage bacap_wb_addon:temp display_format.f int 1 run scoreboard players get #format_frac wb_math_temp

execute if score #format_frac wb_math_temp matches 0..9 run data modify storage bacap_wb_addon:temp display_format.p set value "0"
execute if score #format_frac wb_math_temp matches 10..99 run data modify storage bacap_wb_addon:temp display_format.p set value ""