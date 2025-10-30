import os
from collections.abc import Iterable
from shutil import make_archive
from typing import List, Tuple

from .Advancement import AdvancementsManager
from .Datapack import Datapack
from .InterfaceSchema import *
from .MissingTranslationFinder import MissingTranslationFinder
from .Validator import Validator
from .Warnings import AdvWarning, AdvWarningType
from .utils import fill_pattern


class Release:
    @staticmethod
    def create_install(datapack: Datapack, version: str):
        """
        Updates install.mcfunction with a correct version.
        """
        if not datapack.install_path:
            return

        filename = fill_pattern(datapack.release_name_pattern, {"version": version})
        install_text = fill_pattern(datapack.install_mcfunc_pattern, {"version": version, "filename": filename})
        datapack.install_path.write_text(install_text, encoding=datapack.encoding)

    @staticmethod
    def create_datapack_zip(datapack: Datapack, version: str):
        """
        Create zipped datapack
        """
        output_path = os.path.join(
            os.getcwd(),
            'releases',
            fill_pattern(datapack.release_name_pattern, values={"version": version})
        )

        make_archive(
            base_name=output_path,
            format="zip",
            root_dir=datapack.path,
            base_dir='.'
        )

    @staticmethod
    def create_language_pack_zip(datapack: Datapack):
        """
        Create zipped language pack
        """

        output_path = os.path.join(
            os.getcwd(),
            'releases',
            datapack.language_pack
        )

        make_archive(
            base_name=output_path,
            format="zip",
            root_dir=datapack.language_pack,
            base_dir='.'
        )

    @staticmethod
    def show_adv_warning(adv: Advancement, warning: AdvWarning, indent: int = 0):
        print_warning(adv, indent=indent)
        output(warning.reason, indent=indent + 3)

    @classmethod
    def check(cls, datapack: Datapack | List[Datapack]):
        """
        Check all bacaped advancements and print warnings to console.
        :return: Number of warnings
        """
        warnings_type_dict: dict[str, list[Tuple[Advancement, AdvWarning]]] = {}
        warnings_count = 0

        for adv in AdvancementsManager.filtered_iterator(datapack=datapack, skip_invalid=False):
            warnings = Validator.validate_advancement(adv)
            if not isinstance(adv, InvalidAdvancement):
                warnings.extend(MissingTranslationFinder.find_missing_translations(adv))

            if not warnings:
                continue
            warnings_count += 1

            for warning in warnings:
                if warning.warning_type.name not in warnings_type_dict:
                    warnings_type_dict[warning.warning_type.name] = []
                warnings_type_dict[warning.warning_type.name].append((adv, warning))

        to_show_warning = {}
        warning_type_count = 0
        for warning_type, adv_and_warnings in warnings_type_dict.items():
            n = len(adv_and_warnings)
            if n == 1 and warnings_count < 10:
                cls.show_adv_warning(*adv_and_warnings[0])
                continue

            print_warning(text(warning_type) + f": {n}", icon=Icon(f"[{warning_type_count}]", color="yellow"))
            warning_type_count += 1

            if n <= 3 and warnings_count < 10:
                for adv, warning in adv_and_warnings:
                    cls.show_adv_warning(adv, warning, indent=3)
                continue

            to_show_warning[warning_type] = adv_and_warnings

        if to_show_warning:
            list_n = list(range(len(to_show_warning)))
            possible_values = list(map(str, list_n)) + [""]
            key_list = list(to_show_warning.keys())
            while True:
                option_n = get_value("Warning type:", possible_value=possible_values)
                if option_n == "":
                    break

                for adv, warning in to_show_warning[key_list[int(option_n)]]:
                    cls.show_adv_warning(adv, warning)

        output("All advancements checked")

        if not warnings_count:
            output("No warnings found")

        return warnings_count

    @staticmethod
    def format_datapack_json(datapack: Datapack | Iterable[Datapack]):
        """
        Format all advancements of the datapack
        """

        for adv in AdvancementsManager.filtered_iterator(datapack=datapack):
            adv.format_json()
            adv.functions.main.generate()
            adv.functions.msg.generate()

        for adv in AdvancementsManager.filtered_iterator(datapack=datapack, skip_invalid=False, skip_normal=True):
            if adv.reason.warning_type == AdvWarningType.REWARD_FUNCTION_DOESNT_SET:
                adv.create_reward_function()
