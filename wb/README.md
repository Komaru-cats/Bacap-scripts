**WorldBorder's Addon** is a datapack for [BACAP](https://modrinth.com/datapack/blazeandcaves-advancements-pack) and [BACAPED](https://modrinth.com/datapack/bacap-enhanced-discoveries) that sets the world border to 1 block and gradually expands it as you earn advancements.

This addon adds an extra challenge to your world by limiting exploration until you make progress through the advancement tree. It's designed to encourage progression and exploration in a controlled and rewarding way.

# Features

### Individual rewards mode
Each advancement offers a unique reward based on its difficulty, ranging from fractions of a block to hundreds and even thousands

### Tier rewards mode
Rewards are  linked to the advancement's tier (Task, Goal, Challenge, Super Challenge, etc.), ensuring a more predictable world expansion

## Flexible configuration
All configuration is done via the main menu: `/function bacap_wb_addon:config`

### Fast Expansion Mode
In standard mode, the time it takes for the border to expand is based on the square root of the awarded blocks. Fast mode makes all border expansions happen instantly.

### Radius Bossbar
Allows you to always see the current world size and visually track the ongoing expansion progress via a filling bossbar.

### Reward Settings
- Toggle between the reward modes described above.
- Adjust the global expansion multiplier to make your playthrough easier or harder.
- Reset tier settings to their default values.
- View your current reward settings.

### Scoreboard Settings
Allows you to display a scoreboard tracking exactly how many blocks each player has contributed to the world expansion by completing advancements (recommended for multiplayer).

# Installation process
- Download datapack for your version of minecraft
- For a new world: You can click the "Data Packs" option when creating a new world and select this datapack.
- For an existing world: Paste it into world folder - (world-name)/datapacks.
- Restart world

# FAQ
- Is it possible to complete BACAP(ED) with this Addon?
    - Yes! The datapack is mathematically balanced so that, with enough effort, it is entirely possible to complete 100% of the advancements even on the lowest multiplier on most world seeds.
- How do I complete distance advancements if the border expands so slowly?
    - That's by design! You need to earn enough blocks through regular gameplay to reach the first distance milestones (10,000 blocks). Completing these specific distance advancements will grant you a massive block reward, allowing you to reach the next milestone, and so on. Even in "Tier rewards" mode, these advancements ignore their tier and grant the huge reward!
- What are the standard rewards for advancements in each tier? How many blocks can be obtained by completing all the advancements in a tier?

    | Tier            | BACAP (adv. count × blocks = total) | BACAPED (adv. count × blocks = total) |
    |:----------------|:------------------------------------|:--------------------------------------|
    | Task            | 606 × 1 = 606                       | 645 × 1 = 645                         |
    | Goal            | 349 × 4 = 1396                      | 453 × 3 = 1359                        |
    | Challenge       | 213 × 25 = 5325                     | 213 × 15 = 3195                       |
    | Super Challenge | 38 × 250 = 9500                     | 87 × 100 = 8700                       |
    | Milestone       | 14 × 800 = 11200                    | 29 × 500 = 14500                      |
    | Hiddens         | 13 × 0 = 0                          | 52 × 0 = 0                            |
    | **Sum**         | **28027**                           | **28399**                             |

### Links
- [Komaru Cats Discord](https://discord.gg/j9VKsyXPhz)
- [Komaru Cats GitHub](https://github.com/Komaru-cats/)

# For Contributors
If you wanna suggest a feature, report a bug etc. you can make it either in [Komaru Cats Discord](https://discord.gg/j9VKsyXPhz), [Create an issue](https://github.com/Komaru-cats/WB-Addon-for-BACAP/issues) or [Pull request](https://github.com/Komaru-cats/WB-Addon-for-BACAP/pulls) on GitHub.

# For Fanpack developers
The addon is built with modularity in mind, allowing community fanpacks to seamlessly integrate their own rewards without breaking the core logic.

There are several function tags that can help you integrate your features into the pack (you can find them in `bacap_wb_addon/tags/function`):
1. `detect_mode`: Called a few seconds after entering the world. Used in WB Addon to check if Enhanced Discoveries is installed.
2. `install`: Called only once, upon entering the world for the very first time.
3. `init_blocks`: Called after `detect_mode` inside `post_detect_mode_load` to initialize individual block rewards. The execution order is always `BACAP -> BACAPED -> Fanpacks`.
4. `init_tiers`: Called after `detect_mode` inside `post_detect_mode_load` to initialize tier block rewards. The execution order is always `BACAP -> BACAPED -> Fanpacks`.
5. `post_detect_mode`: Called after `post_detect_mode_load` as the final load function.
6. `reset_tiers_flags`: Called when a player resets the tier reward settings.
7. `1_second_timer` Called every second when datapack is installed.

### How to add a block reward for your custom BACAP Addon
1. Your datapack must support fanpack handling after completing an advancement (e.g., BACAP calls a fanpack function tag after completing any advancement: `$function #bacap_fanpacks:$(reward_id)`).
2. Inside your datapack's `function` folder, create a file containing the advancement reward information. It must look like this:
    ```mcfunction
    execute if score <advancement id> wb matches 1 run return 0
    data modify storage bacap_wb_addon:temp current_adv set value {adv_id:"<advancement id>",title:"<advancement title>",title_color:"<title color>",desc:"<advancement description>",desc_color:"<description color>",tab:"<advancement tab>",type:"<type (add/set)>",tier:"<tier (task, goal, challenge, super_challenge, milestone, hidden, advancement_legend, root)>"}
    function bacap_wb_addon:queue/process_reward with storage bacap_wb_addon:temp current_adv
    ```
   *Example file for the "A Chiptune Relic" advancement:*
    ```mcfunction
    execute if score adventure/a_chiptune_relic wb matches 1 run return 0
    data modify storage bacap_wb_addon:temp current_adv set value {adv_id: "adventure/a_chiptune_relic", title: "A Chiptune Relic", title_color: "#75E1FF", desc: "Excavate an ancient record from within the Trail Ruins", desc_color: "#63BDD7", tab: "Adventure", type: "add", tier: "goal"}
    function bacap_wb_addon:queue/process_reward with storage bacap_wb_addon:temp current_adv
    ```
3. Add a fanpack function tag for the advancement that points to the function you just created. For "A Chiptune Relic", it looks like this:
    - **Path:** `data/bacap_fanpacks/tags/function/adventure/a_chiptune_relic.json`
    - **File content:**
    ```json
    {
      "values": [
        "<your_namespace>:rewards/adventure/a_chiptune_relic"
      ]
    }
    ```
That is all you need for tier block rewards.

**Note: If you want a specific advancement to be exempt from the tier rules, you can do the following**

Add `custom_tier_blocks: <your amount of blocks>` tag to the advancement reward information and change `tier` to `custom`

*Example file for the "Ten Thousand Blocks" advancement (it will increase the world for 70k blocks):*
```mcfunction
execute if score biomes/ten_thousand_blocks wb matches 1 run return 0
data modify storage bacap_wb_addon:temp current_adv set value {adv_id: "biomes/ten_thousand_blocks", title: "Ten Thousand Blocks", title_color: "#75E1FF", desc: "Travel at least 10,000 blocks from the centre of the world in any direction.\nA journey that long begins with a single step", desc_color: "#63BDD7", tab: "Biomes", type: "add", tier: "custom", custom_tier_blocks: 7000000}
function bacap_wb_addon:queue/process_reward with storage bacap_wb_addon:temp current_adv
```

#### For individual block rewards:
**Note: Max. amount of blocks per 1 advancement is 21474836, otherwise it will lead to undefined behavior**
1. Create a function that will contain all of your individual block rewards (e.g., `data/<your_namespace>/function/init_individual_blocks.mcfunction`). The content should be:
    ```mcfunction
    scoreboard players set <advancement id without namespace> wb_adv_blocks <amount of blocks multiplied by 100 for 2-digit precision>
    ```
   *For example, this line sets a 6.00 block reward for the `blazeandcave:adventure/allayance` advancement:*
    ```mcfunction
    scoreboard players set adventure/allayance wb_adv_blocks 600
    ```
2. Add a function tag to inject your `init_individual_blocks` function into the WB Addon's initialization process.
    - **Path:** `data/bacap_wb_addon/tags/function/init_blocks.json`
    - **File content:**
       ```json
       {
         "values": [
           "<your_namespace>:init_individual_blocks"
         ]
       }
       ```


### How to change existing individual rewards
The process is exactly the same as adding new ones. However, since the file containing the advancement information already exists, you only need to create your own function to override the existing rewards and inject it into the `data/bacap_wb_addon/tags/function/init_blocks.json` function tag.

### How to override tier rewards or add new tiers
Tier rewards initialization is called only once per datapack initialization. We use a unique initialization flag (e.g., `#wb_bacap_tiers_init` for BACAP). This guarantees these defaults are applied exactly ONCE. If a player changes them via the UI later, or if a fanpack overrides them on its first load, a `/reload` won't revert them back because the flag is already set to 1.

There are two different types of reward behaviors (defined by the `"type"` field inside the advancement's `.mcfunction` file):
1. **`add` (default):** Advancements of this type will add blocks to the world border size. **These tier values MUST be multiplied by 100** to support decimal places (e.g., 1 block = 100, 5.5 blocks = 550, 10 blocks = 1000).
2. **`set`:** Advancements of this type will set the world border to an exact amount of blocks. **These tier values are NOT multiplied by 100**.

**Note: The maximum amount of blocks per advancement is 21,474,836. Exceeding this limit will lead to undefined behavior. If you accidentally multiply a massive `set` tier value by 100, it will cause an integer overflow and break the datapack's calculations!**

1. Create a function that will contain all of your tier rewards (e.g., `data/<your_namespace>/function/init_tier_blocks.mcfunction`). The content should look like this:
    ```mcfunction
    execute unless score <your initialization flag> wb matches 1 run scoreboard players set #task wb_tier_blocks <blocks multiplied by 100>
    ```
   *For example, this line sets a 4.00 block reward for `goal` advancements:*
    ```mcfunction
    execute unless score #myaddon_tiers_init wb matches 1 run scoreboard players set #goal wb_tier_blocks 400
    ```
   **Note: `add` tiers are multiplied by 100 to support decimal places** (e.g., 1 block = 100, 5.5 blocks = 550, 10 blocks = 1000).
   The `advancement_legend` tier is a `set` tier, so it is **not** multiplied by 100:
    ```mcfunction
    execute unless score #myaddon_tiers_init wb matches 1 run scoreboard players set #advancement_legend wb_tier_blocks 59999968
    ```
   *The default tiers are:* `#task`, `#goal`, `#challenge`, `#super_challenge`, `#milestone`, `#hidden`, and `#advancement_legend`.

   Finally, at the end of the file, mark your tiers as initialized:
    ```mcfunction
    execute unless score <your initialization flag> wb matches 1 run scoreboard players set <your initialization flag> wb 1
    ```

2. Add a function tag to inject your `init_tier_blocks` function into the WB Addon's initialization process.
    - **Path:** `data/bacap_wb_addon/tags/function/init_tiers.json`
    - **File content:**
       ```json
       {
         "values": [
           "<your_namespace>:init_tier_blocks"
         ]
       }
       ```

### How to change the global multiplier via a datapack
The easiest way to do this is by calling the `bacap_wb_addon:config/set_multiplier` function and passing your desired multiplier as a macro argument.

**Note: The multiplier must be between 0.6 and 10.0 with a maximum precision of 2 decimal places.** Values outside this range may make the datapack impossible to complete, cause floating-point precision loss, or break internal calculations.

*For example, this command sets the global multiplier to 2.31:*
```mcfunction
function bacap_wb_addon:config/set_multiplier {value: 2.31}
```

Created by ItzSkyReed, _Fedor_F, Hogurt