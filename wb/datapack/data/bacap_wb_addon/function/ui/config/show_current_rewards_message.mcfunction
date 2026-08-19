tellraw @s {"text":"                                             ","color":"dark_gray","strikethrough":true}
tellraw @s {"text":" "}
tellraw @s {"text":"          Current Reward Settings","color":"gold","bold":true}
tellraw @s {"text":" "}

$tellraw @s [{"text":"  Global Multiplier: ","color":"#8CD8FF"},{"text":"$(mult_w).$(mult_p)$(mult_f)","color":"#95FF73","bold":true},{"text":"×","color":"#95FF73"}]

tellraw @s {"text":" "}
tellraw @s {"text":"  Tier Rewards (in blocks):","color":"#8CD8FF"}

$tellraw @s [{"text":"   • ","color":"dark_gray"},{"text":"Task: ","color":"green"},{"text":"$(task_w).$(task_p)$(task_f)","color":"white"}]
$tellraw @s [{"text":"   • ","color":"dark_gray"},{"text":"Goal: ","color":"#75E1FF"},{"text":"$(goal_w).$(goal_p)$(goal_f)","color":"white"}]
$tellraw @s [{"text":"   • ","color":"dark_gray"},{"text":"Challenge: ","color":"dark_purple"},{"text":"$(chal_w).$(chal_p)$(chal_f)","color":"white"}]
$tellraw @s [{"text":"   • ","color":"dark_gray"},{"text":"Super Challenge: ","color":"#FF2A2A"},{"text":"$(schal_w).$(schal_p)$(schal_f)","color":"white"}]
$tellraw @s [{"text":"   • ","color":"dark_gray"},{"text":"Milestone: ","color":"#E5E74F"},{"text":"$(mile_w).$(mile_p)$(mile_f)","color":"white"}]
$tellraw @s [{"text":"   • ","color":"dark_gray"},{"text":"Hidden: ","color":"light_purple"},{"text":"$(hid_w).$(hid_p)$(hid_f)","color":"white"}]

tellraw @s {"text":" "}
tellraw @s {"text":"                                             ","color":"dark_gray","strikethrough":true}