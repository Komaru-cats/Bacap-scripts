import os.path
from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path
from typing import Set, Tuple, Any

import jsoncomment

from . import Advancement
from .Advancement import AdvancementsManager
from .Datapack import Datapack
from .Warnings import AdvWarning, AdvWarningType


@dataclass(frozen=True)
class CachedTranslation:
    last_modified: float
    main_translation: dict[str, str]
    translation_keys_set: set[str]


class MissingTranslationFinder:
    _cached_main_translation_files: dict[Path, CachedTranslation] = dict()
    _jsoncomment_parser = jsoncomment.JsonComment()

    @classmethod
    def _fetch_translation(cls, datapack: Datapack) -> CachedTranslation:

        last_modified = os.path.getmtime(datapack.main_translation_path)

        if datapack.main_translation_path not in cls._cached_main_translation_files:
            main_translation = cls._read_lang_file(datapack.main_translation_path)
            cls._cache_main_translation_file(datapack.main_translation_path, main_translation, last_modified)

        elif last_modified != cls._cached_main_translation_files[datapack.main_translation_path].last_modified:
            main_translation = cls._read_lang_file(datapack.main_translation_path)
            cls._cache_main_translation_file(datapack.main_translation_path, main_translation, last_modified)

        return cls._cached_main_translation_files[datapack.main_translation_path]

    @classmethod
    def _cache_main_translation_file(cls, main_translation_path: Path, translations: dict[str, str],
                                     last_modified: float):
        cls._cached_main_translation_files[main_translation_path] = CachedTranslation(last_modified, translations,
                                                                                      set(translations.keys()))

    @staticmethod
    def _is_valid_translation_line(line: str) -> bool:
        if not any(char.isalpha() for char in line):
            return False
        if any(substring in line for substring in ["entity.minecraft.", "block.minecraft.", "item.minecraft."]):
            return False
        return True

    @classmethod
    def find_missing_translations(cls, adv: Advancement) -> list[AdvWarning] | None:
        warnings = []
        adv_translations = cls._search_in_dict(adv.json["display"])
        trophy_translations = []
        if adv.functions.trophy.item:
            trophy_translations = [adv.functions.trophy.item.name] + adv.functions.trophy.item.lore.split("\n")

        for adv_translate in adv_translations:
            if not cls._is_valid_translation_line(adv_translate):
                continue

            if adv_translate not in cls._fetch_translation(adv.datapack).translation_keys_set:
                warnings.append(AdvWarning(AdvWarningType.MISSING_TRANSLATION, f"\"{adv_translate.strip("\n")}\" is missing in translation"))

        for trophy_translate in trophy_translations:
            if not cls._is_valid_translation_line(trophy_translate):
                continue

            if trophy_translate not in cls._fetch_translation(adv.datapack).translation_keys_set:
                warnings.append(AdvWarning(AdvWarningType.MISSING_TRANSLATION, f"\"{trophy_translate.strip("\n")}\" is missing in translation in trophy"))
        return warnings

    @classmethod
    def find_all_missing_translations(cls, datapack: Datapack | Iterable[Datapack]) -> list[str]:

        datapack = (datapack,) if isinstance(datapack, Datapack) else datapack

        missing_translations = list()

        for dp in datapack:

            main_translation = cls._fetch_translation(dp)

            translation_lines = cls._find_all_datapack_translation_keys(datapack=dp)
            cls._filter_missing_translations(translation_lines, main_translation.translation_keys_set)

            for filtered_line in cls._filter_missing_translations(translation_lines,
                                                                  main_translation.translation_keys_set):
                if filtered_line not in missing_translations:
                    missing_translations.append(filtered_line)

        return missing_translations

    @classmethod
    def _filter_missing_translations(cls, translation_lines: Iterable[str], main_translation: Set[str]) -> list[str]:
        missing_translations = list()

        for translation_line in translation_lines:
            if cls._is_missing_translation(translation_line, main_translation):
                if translation_line not in main_translation:
                    missing_translations.append(translation_line)
        return missing_translations

    @classmethod
    def _is_missing_translation(cls, translation_line: str, main_translation: Set[str]) -> bool:

        if not cls._is_valid_translation_line(translation_line):
            return False

        if translation_line in main_translation:
            return False

        return True

    @classmethod
    def _find_all_datapack_translation_keys(cls, datapack: Datapack):
        translations = []

        for adv in AdvancementsManager.filtered_iterator(datapack=datapack):
            translations.extend(cls._search_in_dict(adv.json["display"]))
            if adv.functions.trophy.item:
                translations.append(adv.functions.trophy.item.name)
                translations.extend(adv.functions.trophy.item.lore.split("\n"))

        return translations

    @staticmethod
    def _search_in_dict(d: dict) -> list[str]:
        stack = [d]  # Initialize the stack with the starting element d
        translations = []
        while stack:
            current = stack.pop()
            if isinstance(current, dict):
                # If the current item is a dictionary, check if it contains the 'translate' key
                if "translate" in current:
                    translations.append(current["translate"])
                # Add all dictionary values to the stack for further processing
                stack.extend(current.values())
            elif isinstance(current, list):
                # If the current item is a list, add all its elements to the stack
                stack.extend(current)

        return list(reversed(translations))

    @classmethod
    def _read_lang_file(cls, lang_file_path: Path | str, encoding: str = "utf-8") -> dict:
        with open(lang_file_path, encoding=encoding) as file:
            json_data = cls._jsoncomment_parser.load(file)  # Use jsoncomment because of the comments in the land_file
        return json_data
