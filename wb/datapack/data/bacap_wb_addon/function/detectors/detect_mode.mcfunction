scoreboard players set bc_wb wb_is_ed 0
execute if score bacaped bacaped_install matches 1 run scoreboard players set bc_wb wb_is_ed 1

# Fanpacks Handling
function #bacap_wb_addon:detect_mode

# Post-detect handling
function bacap_wb_addon:system/post_detect_mode_load
# Post-detect fanpacks handling
function #bacap_wb_addon:post_detect_mode