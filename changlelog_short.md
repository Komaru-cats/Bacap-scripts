## New Advancements

### Adventure Tab
- Ashes to Ashes - Burn down a Pillager Outpost, a Swamp Hut, and a Woodland Mansion (based on ParzivalAFK's proof-of-concept datapack for an ED update)
- Alpine Settlement - Locate a Village situated in a Meadow (suggested by Rounduction)
- Under the Blossoms - Locate a Village situated in a Cherry Grove (suggest by Rounduction)
- Selenology - Look at each Moon phase through a Spyglass at midnight (suggest by _adamo\_)
- No Discrimination Club - Use a Spyglass to look at a Villager and Pillager without a crossbow sitting in a Boat from at least 50 blocks away (suggest by CoolGirlOmega)
- Monumental Speedrun - Kill 3 Elder Guardians within 30 seconds (suggest by _adamo\_)

### Animals Tab
- A Small Horse Incident - Die of suffocation while on Horse
- The Saddle of Many Races - Kill a Horse of each color variant with a Saddle (suggested by Honestly Tzadok)
- Batminton - Kill a Bat with a deflected Wind Charge from a Breeze
- I Am a Train - Ride a Boat that is connected in a chain with 4 other leashed Boats
- Forbidden Flower - Feed a Bee a Wither Rose

### Biomes Tab
- death.fell.accident.water - Get the "death.fell.accident.water" death message (suggested by MasterKhan)
- Tokyo Drift - Reach a horizontal speed of over 70 blocks per second on Blue Ice in a Boat
- Ice³ - Have a shulker full of blue ice in your inventory
- Neverland Lost - Use a Golden Dandelion a second time on the same mob to resume its aging

### Building Tab
- Heavy Industry - Smelt every Blast Furnace recipe
- Secret Passage! - Walk through a Painting (suggested by _adamo\_)

### Enchanting Tab
- Master Breather - Create a Turtle Shell with all possible enchants at max level (suggested by `Deleted Account`)
- Pimp My Ride - Create a Carrot on a Stick and a Warped Fungus on a Stick with all possible enchantments at their max level
- All the Netherite Armor - Create every Netherite Armor piece variant with all possible enchantments at max level (suggested by Rounduction)

### End Tab
- Void Hammer - Hit a mob with a Mace while taking damage from the End void (suggested by Kishbek)
- A Diverting Misconception - Slay the Ender Dragon while you are in the Overworld (ported from Pokerhok's End Edition datapack)
- Airplane - Glide with an Elytra for 20 minutes continuously
- Persistent Fighters - Kill 5 Shulkers without losing the levitation effect (ported from Pokerhok's End Edition datapack)

### Farming Tab
- I Am on Diet - Don't eat anything for 10 days
- Closed-Loop Economy - Smelt Leaves into Leaf Litter... only to use it as fuel!

### Mining Tab
- Metal Nameplate - Craft a Name Tag using every type of Nugget (based on ParzivalAFK's proof-of-concept datapack for an ED update)
- High-Effort Inefficiency - Smelt Lapis Ore (suggested by Rounduction)
- Pitmaster - Cook every Smoker recipe
  Where Did the Ground Go? - Mine out every block in a single chunk in the Overworld, down to the Bedrock layer
- Where Did the WORLD GO? - Mine out every block in a single chunk in the Overworld, including the Bedrock (hidden)
- Logistics Nightmare - Move a Mineshaft chest minecart from another biome into Sulfur Caves to try to get the Bounce Music Disc
- Bomb Has Been Defused - Kill a primed Sulfur Cube before it explodes (suggested by Ellie)
- The Gravity of the Situation - Be within 16 blocks of every falling block variant at once (suggested by _adamo\_)
- Mind the Gap - Place opposing Pointed Dripstones while crouching to keep them separated

### Nether Tab
- Lord of the Rings - Visit a Stronghold in every ring around the world's center
- Primitive Excavation - Use a Bed as an explosive mining tool

### Potion Tab
- Seasick - Have nausea while riding a Boat


### Redstone Tab
- Back to Basics - Shear a Mooshroom to turn it back into a regular Cow (based on ParzivalAFK's proof-of-concept datapack for an ED update)
- Classic Door Trap - Fall for the oldest trick in the book: the Iron Door trap (based on ParzivalAFK's proof-of-concept datapack for an ED update)
- Timing Is Everything - Adjust a Redstone Repeater to all four delay settings (based on ParzivalAFK's proof-of-concept datapack for an ED update)
- Staring Contest - Create a Redstone clock by placing two Observers facing each other (based on ParzivalAFK's proof-of-concept datapack for an ED update)
- Idea Generator - Light a Copper Bulb on top of your head (suggested by _adamo\_)

### Super Challenges Tab
- Third Escape Velocity - Reach a vertical speed of over 16,700 blocks per second

### Statistics Tab
- A Delicate Touch - Brush 10 Suspicious blocks (suggested by _adamo\_)
- Careful Excavator - Brush 50 Suspicious blocks (suggested by _adamo\_) 
- Master Archaeologist - Brush 250 Suspicious blocks (suggested by _adamo\_)
- Living History - Brush 1000 Suspicious blocks (suggested by _adamo\_)

- ### Datapack Menu (/function bacaped:config)
    Added datapack menu to configure ED scoreboards:
    - ED Advancements - keeps track of how many ED advancements each player has obtained 
    - All ED Advancements - keeps track of the total number of advancements (including hidden) each player has obtained
    - Hidden ED Advancements - keeps track of how many hidden ED advancements each player has obtained
    - ED Advancement Points - keeps track of how many ED advancement points each player has earned

## Changes
- Rebalanced Super Challenges tab (moved a lot of advancements to different tabs)
- Changed some Statistics advancements names to better one
- Changed trophy descriptions to better one
- Rebalanced XP, Item rewards
- Added missing Mobs/Items/Blocks to some advancement requirements
- Added more "Actual Requirements" descriptions

## Fixes
- Used biome tags where possible instead of their list
- The "Incredibly Big Salmon" trophy rewarded by "Master Fisherman" is now actually a large salmon
- Fixed "Heavy Catch" wasn't working
- Removed `map_color` component from "Master Shieldman" trophy
- Fixed "Dead Carnival" file name: `dead_carnaval` -> `dead_carnival`
- Fixed "Explosive Elixir" file name: `explosive_elexir` -> `explosive_elixir`
- Fixed "Extinction" file name: `extincion` -> `extinction`
- Removed all enchantments from "Professional Fishing Rod" trophy to avoid granting "Master Fisherman" advancement 
- Fixed progress cheese for "Distorted Cave Maze", "The Infernal Cauldron", and "One Minute Warden Hugs" while being dead
- Separated "Its Midnight Already" trophy description to 24 lines
- Run additional commands from fanpacks before granting advancement for all other players in coop in `advancement_made_macro`
- Added all missing pre-3.0 translations 
- Fixed completion messages for advancements overridden by the Hardcore Addon
- Deleted outdated/unused files from datapack
- Fixed incorrect tab display name for "BlazeandCave's Advancements" tab in advancement completion messages
- Changed all `’` symbols to `'`

#### and a lot more! [Click if you want to read full changelog]()
