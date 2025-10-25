# Bacap-scripts 
This repository contains the source code for generating datapacks as well as the datapacks themselves. Changes to a datapack are usually made here and then a pull request is submitted to the main repository.

The code can generate files for advancements, trophies, and messages. It includes a wide range of features but may not support certain functions or Minecraft versions.


## Features
- The script allows you to add trophies and rewards with fully customizable data, such as name, color, description, enchantments, and more.
- It automatically generates messages for advancements.
- There is a feature for detecting missing translations, although it may not work correctly as it hasn’t been updated in a while.
- You can set a number of blocks for missing advancements for the WorldBorder addon in script.
- During release, the script performs the following automatically:
    - Updates milestones
    - Generates necessary files for translations
    - Creates reward and message files (if they do not exist)
    - Formats advancements
    - Creates a zipped release of the datapack
    - Generates advancement data for the website

## How to Run
To launch the interface for **Enhanced Discovery**:

```bash
python scripts/AdvancementInterface.py
```
> The working directory must be the root of the repository.

To run the **WorldBorder** script:

```bash
python -m scripts.WorldBorder
```

> Again, make sure the working directory is the root of the repository.

## Configuration

You can configure `user_config.json` to specify the paths to the resource pack and datapack located within a Minecraft world, which is useful for testing. The values should be **paths to the folders** of the datapack/resource pack, not just the directories containing them. For example:
```json
{
  "mcpath": "path_to_a_minecraft/saves/world/datapacks/bacaped",
  "rppath": "path_to_a_minecraft/resourcepacks/bacaped_translate"
}
```

> Be careful, this script completely deletes the folders specified in the config file

## Project Structure and Notes

- The `datapacks` folder should contain the latest versions of the datapacks, including **Bacap**.
- The file `pages/assets/requirements.json` must be updated **manually** to reflect changes on the advancements page.
- Datapack releases are stored in the `releases` folder.
- The `resources` folder contains data about Minecraft items. This list should be updated when Minecraft is updated to ensure correct functionality.
- The **WorldBorder addon** uses a local SQLite database — the code is designed to work with it.

## Repository Notes
- This repository includes a `ForceResolve #issue_number` feature:  
  If a commit message contains `ForceResolve #<issue_number>`, the corresponding issue will be automatically closed.
  For example: `feat: ForceResolve #575 - add new advancement`
- There is a GitHub Actions workflow called `push_to_main_rep.yml` for pushing changes to the main repository.
