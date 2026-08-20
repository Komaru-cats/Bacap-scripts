tellraw @s {"text":"                                             ","color":"dark_gray","strikethrough":true}
tellraw @s {"text":" "}
tellraw @s {"translate":"          Current Reward Settings","color":"gold","bold":true}
tellraw @s {"text":" "}

$tellraw @s [{"translate":"  Global Multiplier: ","color":"#8CD8FF"},{"text":"$(mult_w).$(mult_p)$(mult_f)","color":"#95FF73","bold":true},{"text":"×","color":"#95FF73"}]

tellraw @s {"text":" "}
tellraw @s {"translate":"  Tier Rewards (in blocks):","color":"#8CD8FF"}

$tellraw @s [{"text":"   • ","color":"dark_gray"},{"translate":"Task: ","color":"green"},{"text":"$(task_w).$(task_p)$(task_f)","color":"white"}]
$tellraw @s [{"text":"   • ","color":"dark_gray"},{"translate":"Goal: ","color":"#75E1FF"},{"text":"$(goal_w).$(goal_p)$(goal_f)","color":"white"}]
$tellraw @s [{"text":"   • ","color":"dark_gray"},{"translate":"Challenge: ","color":"dark_purple"},{"text":"$(chal_w).$(chal_p)$(chal_f)","color":"white"}]
$tellraw @s [{"text":"   • ","color":"dark_gray"},{"translate":"Super Challenge: ","color":"#FF2A2A"},{"text":"$(schal_w).$(schal_p)$(schal_f)","color":"white"}]
$tellraw @s [{"text":"   • ","color":"dark_gray"},{"translate":"Milestone: ","color":"#E5E74F"},{"text":"$(mile_w).$(mile_p)$(mile_f)","color":"white"}]
$tellraw @s [{"text":"   • ","color":"dark_gray"},{"translate":"Hidden: ","color":"light_purple"},{"text":"$(hid_w).$(hid_p)$(hid_f)","color":"white"}]

tellraw @s {"text":" "}
tellraw @s {"text":"                                             ","color":"dark_gray","strikethrough":true}