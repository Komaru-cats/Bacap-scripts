import json
import re
import shutil
import threading
from pathlib import Path
from textwrap import wrap as textwrap

import pyperclip

import tools.data_writer as dw
from tools import Advancement, AdvancementsManager, AdvancementFactory, DatapackList, Resources, Patterns
from tools.BaseTranslationGenerator import BaseTranslationGenerator
from tools.ComponentsInterface import ComponentsInterface as Ci
from tools.DatapackFunctionsGenerator import DatapackFunctionsGenerator
from tools.Interface import MenuInterface, exit_on_empty_input
from tools.Interface import func_loop as loop
from tools.InterfaceSchema import *
from tools.MilestonesGenerator import MilestonesGenerator
from tools.MissingTranslationFinder import MissingTranslationFinder
from tools.Release import Release
from tools.Validator import Validator, SpellingValidator
from tools.utils import cut_namespace, multi_replace, user_config

change_type_mi = MenuInterface(input_icon=Icon("[>]", color="cyan"))
adv_mi = MenuInterface(input_icon=Icon("[>]", color="purple"))
func_mi = MenuInterface(input_icon=Icon("[>]", color="cyan"))
mi = MenuInterface(input_icon=Icon("[>]"))


@change_type_mi.register_class()
class Renaming:
    @change_type_mi.register_func("path", "p")
    @exit_on_empty_input
    def change_path(self, adv: Advancement):
        path = eget_value("Path:")
        old_mc_path = adv.mc_path
        adv_path_folder = adv.datapack.default_advancements_path
        path = adv_path_folder / f"{path}.json"
        if (not path.parent.exists()) or (not path.is_relative_to(adv_path_folder)) or (
                path.resolve() == adv_path_folder.resolve()):
            print_warning(f"Can't find folder {path.parent}")
            return
        if not eget_bool(f"Continue with '{path.relative_to(adv_path_folder).with_suffix("").as_posix()}' [y/n]:"):
            return
        adv.path = path
        parent = get_value("New parent [empty/any]:")
        if parent:
            adv.parent = parent

        output(f"Advancement renamed: {old_mc_path} -> {adv.mc_path}")

    @change_type_mi.register_func("title", "t")
    @exit_on_empty_input
    def change_title(self, adv: Advancement):
        title = eget_value("Title:", exit_on_empty=True)
        warnings = SpellingValidator.validate_title(title, adv.datapack)
        if warnings:
            print_warning(text(
                f"Title \"{title}\" has {len(warnings)} warnings:\n {"\n".join([warning.reason for warning in warnings])}"))
        if not eget_bool(f"Continue with '{title}' [y/n]:"):
            return
        adv.title = title

    @change_type_mi.register_func("description", "d")
    @exit_on_empty_input
    def change_description(self, adv: Advancement):
        description = eget_value("Description:")
        if not eget_bool(f"Continue with '{description}' [y/n]:"):
            return
        adv.description = description

    @change_type_mi.register_func("type", "type")
    @exit_on_empty_input
    def change_type(self, adv: Advancement):
        types = adv.datapack.adv_default_type_data.keys()
        output("Possible types: " + ", ".join(types))
        adv_type = eget_value("Type:", possible_value=types)
        if not eget_bool(f"Continue with '{adv_type}' [y/n]:"):
            return
        hidden = eget_bool("Is hidden [y/n]:")
        adv.hidden = hidden
        adv.type = adv_type


@adv_mi.register_class()
class AdvancementInterface:

    @staticmethod
    def search_adv(find, datapacks=None):
        AdvancementsManager.generate()  # Updating the list before searching
        if datapacks is None:
            datapacks = DatapackList.available
        criteria_list = ("title", "filename", "reward_mcpath", "description")
        for criteria in criteria_list:
            adv_list = AdvancementsManager.find({criteria: find}, datapacks, limit=1)
            if adv_list:
                return adv_list[0]
        for criteria in criteria_list:
            adv_list = AdvancementsManager.deep_find({criteria: find}, datapacks, limit=1)
            if adv_list:
                return adv_list[0]
            return None
        return None

    @staticmethod
    def __filename_by_adv_title(title):
        forbidden_chars_in_file = ((",", ""), ("?", ""), ("'", ""), ("!", ""), ("\"", ""))
        return "_".join(multi_replace(title.lower(), forbidden_chars_in_file).split(" "))

    @adv_mi.register_func("Info", "i")
    def advancement_info(self):
        AdvancementsManager.generate()  # Updating the list before getting info
        while True:
            find_input = get_value("Advancement:")
            if find_input == "":
                return
            adv = self.search_adv(find_input)
            if not adv:
                continue
            print_adv_data(adv)

    @adv_mi.register_func("Stats", "stats")
    def stats(self):
        AdvancementsManager.generate()  # Updating the list before getting stats
        from collections import defaultdict
        split_hidden = get_bool("See hidden separately [y/n]:")
        for datapack in DatapackList.work_with:
            adv_types = defaultdict(list)

            if split_hidden:
                for adv in AdvancementsManager.find(criteria={"hidden": False}, datapack=datapack):
                    adv_types[adv.type].append(adv)

                adv_types["hidden"] = AdvancementsManager.find(criteria={"hidden": True}, datapack=datapack)
            else:
                for adv in AdvancementsManager.filtered_iterator(datapack=datapack):
                    adv_types[adv.type].append(adv)

            adv_type_count = {key: len(value) for key, value in adv_types.items()}
            adv_type_count = dict(sorted(adv_type_count.items(), key=lambda item: item[1], reverse=True))
            output(f"{datapack}: {sum(x for x in adv_type_count.values())}")
            output("\n".join(f"{adv_type}: {n}" for adv_type, n in adv_type_count.items()), indent=3)

    @adv_mi.register_func("Rename", "r")
    @exit_on_empty_input
    def renaming(self):
        AdvancementsManager.generate()  # Updating the list before renaming something
        while True:
            find_input = eget_value("Advancement:")
            adv = self.search_adv(find_input, datapacks=DatapackList.default)
            if not adv:
                continue
            print_adv_data(adv)
            change_type_mi.menu(adv)

    @adv_mi.register_func("Delete", "d")
    @exit_on_empty_input
    def delete(self):
        AdvancementsManager.generate()  # Updating the list before deleting something
        while True:
            find_input = eget_value("Advancement:")
            adv = self.search_adv(find_input, datapacks=DatapackList.default)
            if not adv:
                continue
            print_adv_data(adv)
            if eget_bool("Continue deleting [y/n]:"):
                adv.delete()

    @adv_mi.register_func("Check", "c")
    def check(self):
        AdvancementsManager.generate()  # Updating the list before checking it
        Release.check(DatapackList.work_with)

    @adv_mi.register_func("Update", "u")
    def update_advancements(self):
        AdvancementsManager.generate()  # Updating the list in the interface
        output("Update is done", indent=3)

    @adv_mi.register_func("Add", "a")
    @loop
    def create(self):
        @exit_on_empty_input
        def create_adv(advancement_json):
            warnings = Validator.validate_json_structure(adv_json=advancement_json, datapack=DatapackList.default)
            if warnings:
                print_warning("\n".join(map(str, warnings)))
                if not get_bool("Continue [y/n]:"):
                    return
            name = self.__filename_by_adv_title(advancement_json["display"]["title"]["translate"])
            parent_adv = AdvancementsManager.find({"mc_path": advancement_json["parent"]},
                                                  datapack=DatapackList.available, limit=1)
            if parent_adv:
                folder = (DatapackList.default.default_advancements_path / cut_namespace(
                    parent_adv[0].reward_mcpath)).parent
                path = folder / f"{name}.json"
            else:
                folder = DatapackList.default.default_advancements_path / eget_value("Path to advancement folder:")
                path = folder / f"{name}.json"

            while True:
                output(path, icon=Icon("[p]"))
                cont = eget_value_from_variants(f"Continue [y/n]:", y=True, n=False)
                if cont == "e":
                    break
                elif not cont:
                    path = DatapackList.default.default_advancements_path / (
                                eget_value(f"Path (with filename):") + ".json")

                if not advancement_json.get("rewards"):
                    reward = f"{DatapackList.default.reward_namespace}:{path.relative_to(DatapackList.default.default_advancements_path).with_suffix("").as_posix()}"
                    advancement_json["rewards"] = {"function": reward}
                AdvancementFactory.add_advancement(path, advancement_json, datapack=DatapackList.default)
                shutil.copy(path, Path(user_config["mcpath"]) / Path("/".join(path.parts[2:])))
                break

        if get_value("Copy json and continue [any/e]:") != "e":
            adv = pyperclip.paste()
        else:
            return True
        try:
            adv_json = json.loads(adv)
            create_adv(adv_json)
        except json.JSONDecodeError as json_error:
            print_warning(f"Invalid json, try again\n{json_error.msg} at {json_error.lineno}:{json_error.colno}")

    @adv_mi.register_func("Format", "format")
    def advancement_format(self):
        AdvancementsManager.generate()  # Updating the list before formatting it
        Release.format_datapack_json(DatapackList.work_with)

    @adv_mi.register_func("Milestone", "mil")
    def milestones_create(self):
        MilestonesGenerator.generate_all(DatapackList.default)


@func_mi.register_class()
class FuncInterface:

    @staticmethod
    def __color_wrapper(color):
        mc_colors = Resources.TextColors.list
        if color in mc_colors:
            return color
        elif re.search(Patterns.BasePatterns.color, color):
            if color[0] == "#":
                return color
            else:
                return "#" + color
        else:
            raise ValueError(f"{color} isn't color")

    @staticmethod
    @loop
    def __make_text_with_lines():
        lines = []
        i = 1
        output("Add lines yourself:")
        while get_bool("Add string [y/n]:", indent=3):
            lines.append(get_value(f"Line {i}:", indent=3))
            i += 1
        input_text = "\n".join(lines)
        if get_bool("Continue with:\n" + input_text + "\n[y/n]:", indent=3):
            return lines

    @staticmethod
    def __generate_main(adv: Advancement):
        adv.functions.main.generate()

    @staticmethod
    def __generate_msg(adv: Advancement):
        adv.functions.msg.generate()

    @staticmethod
    @exit_on_empty_input
    def __generate_exp(adv: Advancement):
        exp = eget_value("Exp:", value_type=int)
        if exp == 0:
            adv.functions.exp.generate(None)
        adv.functions.exp.generate(exp)
        return True

    @exit_on_empty_input
    @loop
    def __generate_reward(self, adv: Advancement):
        if not eget_bool("Give Reward [y/n]:"):
            adv.functions.reward.generate(None)
            return True
        item_id = eget_value("Item Id:", possible_value=Resources.ItemProperties.list)
        amount = eget_value("Amount:", value_type=int)
        command = "give"
        components = None

        if eget_bool("Add extra data [y/n]:"):
            command = eget_value_from_variants("Give or Summon command [g/s]:", s="summon", g="give")
            components = Ci(item_id)

        output(f"Data:")
        output(f"Item Id: {item_id}", icon=Icon("[i]", color="purple"), indent=3)
        output(f"Amount: {amount}", icon=Icon("[a]", color="purple"), indent=3)
        output(f"Command: {command}", icon=Icon("[c]", color="purple"), indent=3)
        if eget_bool("Continue with this data [y/n]:"):
            adv.functions.reward.generate(item_id, amount, command, components)
            return True
        return None

    @exit_on_empty_input
    @loop
    def __generate_trophy(self, adv: Advancement):
        if not eget_bool("Give Trophy [y/n]:"):
            adv.functions.trophy.generate(None)
            return True
        item_id = eget_value("Item Id:", possible_value=Resources.ItemProperties.list)
        name = eget_value("Name:")
        description = textwrap(eget_value("Description:"), 45)
        output(f"Description:\n{"\n".join(description)}", icon=Icon("[d]", color="purple"))
        if not eget_bool("Use this split text [y/n]:"):
            description = self.__make_text_with_lines()
        color = eget_value("Color:", value_type=self.__color_wrapper)
        command = eget_value_from_variants("Give or Summon command [g/s]:", s="summon", g="give")
        components = Ci(item_id, True)

        output(f"Data:")
        output(f"Item Id: {item_id}", icon=Icon("[i]", color="purple"), indent=3)
        output(f"Name: {name}", icon=Icon("[n]", color="purple"), indent=3)
        output(f"Description:\n{"\n".join(description)}", icon=Icon("[d]", color="purple"), indent=3)
        output(f"Color: {color}", icon=Icon("[c]", color="purple"), indent=3)
        output(f"Command: {command}", icon=Icon("[c]", color="purple"), indent=3)

        trophy_command = adv.functions.trophy.generate(item_id, name, description, color, command, components)
        pyperclip.copy(trophy_command.splitlines()[0])
        output("Command to give trophy has been copied")
        if eget_bool("Continue with this trophy [y/n]:"):
            return True

    @func_mi.register_func("Change Rewards", "c")
    @exit_on_empty_input
    @loop
    def change_rewards(self):
        while True:
            adv = eget_value("Advancement:")
            adv = AdvancementInterface.search_adv(adv, DatapackList.default)
            if adv:
                break
        print_adv_data(adv)
        if not eget_bool("Continue [y/n]:"):
            return
        func = eget_value_from_variants("Exp | Reward | Trophy [e/r/t]:",
                                        e=self.__generate_exp, r=self.__generate_reward, t=self.__generate_trophy)
        func(adv)

    @func_mi.register_func("Generate All", "all")
    @exit_on_empty_input
    def generate_all(self):
        for adv in AdvancementsManager.filtered_iterator(datapack=DatapackList.default):
            functions = adv.functions
            if adv.datapack.generate_functions and not any(
                    (functions.exp.empty, functions.reward.empty, functions.trophy.empty)):
                continue
            print_adv_data(adv)
            if not eget_bool("Continue [y/n]:"):
                continue
            self.__generate_main(adv)
            self.__generate_msg(adv)
            if functions.exp.empty:
                output("Exp")
                self.__generate_exp(adv)
            if functions.reward.empty:
                output("Reward")
                self.__generate_reward(adv)
            if functions.trophy.empty:
                output("Trophy")
                self.__generate_trophy(adv)
        output("All generated")

    @func_mi.register_func("Regen Trophies", "r")
    def regen_trophies(self):
        AdvancementsManager.generate()  # Обновляем сука ачивки перед тем как...
        for adv in AdvancementsManager.filtered_iterator(datapack=DatapackList.default):
            adv.functions.trophy.gen_from_selfdata()


@mi.register_class()
class MainInterface:
    @mi.register_func("Advancement", "a")
    def advancement_menu(self):
        adv_mi.menu()

    @mi.register_func("Functions", "f")
    def advancement_menu(self):
        func_mi.menu()

    @mi.register_func("Create Release", "release")
    def release(self):
        AdvancementsManager.generate()  # Updates all the advancement before release

        BaseTranslationGenerator.update(DatapackList.default)
        output("Base Translation updated")

        MilestonesGenerator.generate_all(DatapackList.default)
        output("Milestones created")

        DatapackFunctionsGenerator.generate_all(DatapackList.default)
        output("Datapack Functions created")

        Release.format_datapack_json(DatapackList.work_with)
        output("All Advancements formatted")

        for datapack in DatapackList.work_with:
            output(datapack, icon=Icon("[D]"))
            if count := Release.check(datapack):
                if not get_bool(f"You have {count} {"problem" if count == 1 else "problems"}\n"
                                f"Do you want to continue create release [y/n]:",
                                icon=Icon("[>]", color="yellow", bold=True), indent=3):
                    return
            version = get_value("Version:", indent=3)
            Release.create_install(datapack, version)
            output("Install created", indent=3)
            Release.create_datapack_zip(datapack, version)
            Release.create_language_pack_zip(datapack)
            output("Zip created", indent=3)
        output("Release created")

        dw.create()
        output("data.json has been updated")

    @mi.register_func("Save to mc", "s")
    def save_to_mc(self):
        def save_operation():
            datapack_path = Path(user_config["mcpath"])
            resourcepack_path = Path(user_config["rppath"])

            for file in datapack_path.iterdir():
                if file.name == "pack.mcmeta":
                    break
            else:
                print_warning("The datapack path in user's config is invalid. Can't find pack.mcmeta\n"
                              "If it's correct path - add pack.mcmeta", color="yellow")
                return

            if datapack_path.exists():
                shutil.rmtree(datapack_path)
            shutil.copytree(DatapackList.default.path, datapack_path, dirs_exist_ok=True)

            shutil.copytree(resourcepack_path.name, resourcepack_path, dirs_exist_ok=True)

        threading.Thread(target=save_operation).start()

    @mi.register_func("Find Missing Translation", "t")
    def find_missing_translation(self):
        missing_translations = MissingTranslationFinder.find_all_missing_translations(datapack=DatapackList.work_with)

        if missing_translations:
            print_warning(text("Missing translations:\n", bold=True) + "\n".join(
                [f"\"{x}\": \"\"," for x in missing_translations]))
        else:
            output(text("All translations are fine", bold=True))


if __name__ == "__main__":
    AdvancementsManager.generate(force=True)
    mi.menu()
