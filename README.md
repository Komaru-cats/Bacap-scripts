# Bacap-scripts

This repository contains the source files, configurations, and assets for generating and maintaining **Enhanced Discoveries** (`bacaped`) and **WorldBorder Addon** datapacks. Changes to the datapacks are made here before submitting a pull request to the main repository.

The project now uses dedicated interactive CLI utilities (**BACAP-Addon-Helper** and **WB-Addon-Helper**) to manage advancements, trophies, rewards, translations, and releases.

---

## Getting Started

### 1. Download Helper Binaries

Before running the tools, download the latest helper executables (`bacap_addon_helper` and `wb_addon_helper`). The download script automatically detects your OS, CPU architecture, and whether the **.NET 10** runtime is installed (fetching lightweight framework-dependent binaries if found, or self-contained binaries otherwise).

**Using JetBrains IDE (`.run` configurations):**
Run the **Download Helpers [Windows]** or **Download Helpers [Unix]** run configuration.

**Via Terminal (from the repository root):**
- **Windows:**
  ```cmd
  scripts\download_helpers.bat
  ```
- **Linux / macOS:**
  ```bash
  ./scripts/download_helpers.sh
  ```

---

### 2. Environment Configuration (`.env`)

Global tool configuration is located in the `config/` directory (`bacap_addon_helper_config.yaml` and `wb_addon_helper_config.yaml`) and are already configured.

For syncing datapacks and resource packs directly to local Minecraft worlds, create `.env` files in the repository root based on the provided examples:

#### Enhanced Discoveries (`.env.bacap_addon`)
Copy `.env.bacap_addon.example` to `.env.bacap_addon`:
```env
WORLD_DATAPACKS_PATH="path/to/world/datapacks/folder/without/compatibility/addons"
WORLD_COMPAT_DATAPACKS_PATH="path/to/world/datapacks/folder/with/compatibility/addons"
RESOURCE_PACKS_PATH="path/to/resourcepacks/folder"
```

#### WorldBorder Addon (`.env.wb_addon`)
Copy `.env.wb_addon.example` to `.env.wb_addon`:
```env
WORLD_DATAPACKS_PATH="path/to/world/datapacks/folder/with/wb/addon"
```

> **Warning:** When syncing packs to your Minecraft saves folder, the utilities overwrite the target directories specified in your `.env` files.

---

### 3. How to Run

Ensure your working directory is the **root of the repository**.

#### Option A: JetBrains IDE Run Configurations (Recommended)
Ready-to-use configurations are located in `.run/`:
- **Run BACAP Helper [Windows]** / **Run BACAP Helper [Unix]** — launches Enhanced Discoveries helper.
- **Run WB Helper [Windows]** / **Run WB Helper [Unix]** — launches WorldBorder Addon helper.

#### Option B: Terminal

- **Enhanced Discoveries (BACAP Addon Helper):**
    - **Windows:**
      ```cmd
      scripts\run_bacap_helper.bat --config config/bacap_addon_helper_config.yaml
      ```
    - **Linux / macOS:**
      ```bash
      ./scripts/run_bacap_helper.sh --config config/bacap_addon_helper_config.yaml
      ```

- **WorldBorder Addon (WB Addon Helper):**
    - **Windows:**
      ```cmd
      scripts\run_wb_helper.bat --config config/wb_addon_helper_config.yaml
      ```
    - **Linux / macOS:**
      ```bash
      ./scripts/run_wb_helper.sh --config config/wb_addon_helper_config.yaml
      ```

---

## Project Structure

- `assets/` — Source datapacks (`bacap_datapack` as read-only reference, `bacaped_datapack`, `bacaped_hardcore_datapack`, `wb_addon_datapack`) and the language resource pack (`bacaped_lang_pack`).
- `config/` — YAML configuration files for the CLI helpers.
- `registries/` — Extracted Minecraft registry JSON files (items, blocks, potions, etc.), updateable via [registry-dumper](https://github.com/ItzSkyReed/registry-dumper).
- `requirements/` & `docs/` — Actual requirements input and generated advancement documentation output for the website.
- `releases/` — Destination folder for packed `.zip` releases.
- `scripts/` — Helper download and launcher scripts (`.bat` / `.sh`); downloaded binaries are placed into `scripts/helpers/`.
- `wb_addon.db` — Local SQLite database storing block counts and configurations for the WorldBorder addon.

---

## Repository Notes

- **Issue Auto-Close (`ForceResolve`)**:  
  If a commit message contains `ForceResolve #<issue_number>`, the corresponding issue will be automatically closed by GitHub Actions.  
  *Example:* `feat: ForceResolve #575 - add new advancement`
