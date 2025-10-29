import json
import re
from itertools import chain
from pathlib import Path
from typing import Set, Literal, List, Tuple

import titlecase

from .Advancement import Advancement, AdvancementsManager, InvalidAdvancement
from .Datapack import DatapackList, Datapack
from .Resources import ItemProperties
from .Warnings import AdvWarningType, AdvWarning
from .utils import can_access_keypath, cut_namespace
from .utils import get_by_keypath


class Validator:

    @classmethod
    def validate_advancement(cls, advancement: Advancement | InvalidAdvancement) -> list[AdvWarning]:
        if isinstance(advancement, InvalidAdvancement):
            return [AdvWarning(AdvWarningType.INVALID_ADVANCEMENT_IN_RELEASE, f"Reason: {advancement.reason.reason}")]

        warnings = []

        result = cls._validate_reward_function(advancement)
        if result:
            warnings.extend(result)

        result = cls._validate_parent(advancement)
        if result:
            warnings.append(result)

        if advancement.tab in advancement.datapack.tabs_have_branch:
            result = cls._validate_branch_existence(advancement)
            if result:
                warnings.append(result)
        warnings.extend(SpellingValidator.validate_misspelling(advancement))

        return warnings

    @staticmethod
    def _validate_reward_function(adv: Advancement) -> list[AdvWarning]:
        """
        Function to check advancement's correctness.
        Checks: reward-functions, json-keys, advancement's type and parent.
        :param adv: The instance of Advancement.
        :return: List with warnings.
        """
        warnings = []

        if not can_access_keypath(adv.json, ["rewards", "function"]):
            warnings.append(AdvWarning(AdvWarningType.REWARD_FUNCTION_DOESNT_SET, "Reward function doesn't set"))

        elif adv.reward_mcpath != (expect := f"{adv.datapack.reward_namespace}:{cut_namespace(adv.mc_path)}"):
            warnings.append(AdvWarning(AdvWarningType.REWARD_FUNCTION_DOESNT_MATCH, "Reward function doesn't match:\n"
                                                                                    f"Expected '{expect}'\n"
                                                                                    f"Got '{adv.reward_mcpath}'"))

        elif files := adv.functions.get_non_existent_files():
            warnings.append(AdvWarning(AdvWarningType.DONT_FILES_EXIST, "Doesn't all files exist: " + ", ".join(files)))

        elif files := adv.functions.get_empty_files():
            warnings.append(AdvWarning(AdvWarningType.EMPTY_FILES, "Some files empty: " + ", ".join(files)))

        return warnings

    @staticmethod
    def _validate_parent(adv: Advancement) -> AdvWarning | None:
        if adv.filename == "root":
            return
        elif not AdvancementsManager.find(criteria={"mc_path": adv.parent}, datapack=DatapackList.available,
                                          skip_technical=False, skip_invalid=False, limit=1):
            return AdvWarning(AdvWarningType.INVALID_PARENT, f"Invalid parent: {adv.parent}")
        return

    @staticmethod
    def _find_last_advancement(adv: Advancement) -> Advancement:
        """
        Finds the last advancement in the chain starting from the given advancement.
        This method follows the parent chain until it reaches the root.
        :param adv: The starting advancement.
        :return: The last advancement in the chain.
        """
        adv_map = {adv.mc_path: adv for adv in
                   AdvancementsManager.filtered_iterator(datapack=DatapackList.available, skip_technical=False)}

        while adv.parent in adv_map:
            adv = adv_map[adv.parent]

        return adv

    @staticmethod
    def _find_root_advancement(adv: Advancement) -> Advancement:
        """
        Recursively finds the root advancement by traversing through parents until a non-hidden challenge is found.
        """
        while adv.hidden:
            parent_advancements = AdvancementsManager.find({"mc_path": adv.parent}, datapack=DatapackList.available,
                                                           limit=1)
            if not parent_advancements:
                break
            adv = parent_advancements[0]
        return adv

    @classmethod
    def _validate_branch_existence(cls, adv: Advancement) -> AdvWarning | None:
        """
        Checks if given advancement belongs to a branch.
        It returns a warning if the advancement does not belong to any branch.
        :param adv: The advancement to check.
        :return: List of warning advancements.
        """

        last_adv = cls._find_last_advancement(adv)

        branch_parent_list = {tech_adv.parent for tech_adv in
                              AdvancementsManager.filtered_iterator(datapack=DatapackList.available,
                                                                    skip_technical=False) if tech_adv.parent}

        if last_adv.mc_path not in branch_parent_list:
            root_adv = cls._find_root_advancement(last_adv)
            if root_adv.mc_path not in branch_parent_list:
                return AdvWarning(AdvWarningType.MISSING_BRANCH, f"Doesn't have branch in {adv.tab} tab")

        return

    @staticmethod
    def validate_json_structure(adv_json: dict = None, datapack: Datapack = None) -> List[AdvWarning]:
        """
        Function to check advancement's JSON's correctness.
        :param datapack: Datapack class
        :param adv_json: JSON of advancement presented as dict
        :return: List with warnings.
        """

        warnings = []
        frame = get_by_keypath(adv_json, ("display", "frame"))
        color = get_by_keypath(adv_json, ("display", "description", "color"))

        frame_list = ["task", "goal", "challenge"]

        if frame and frame not in frame_list:
            warnings.append(AdvWarning(AdvWarningType.UNKNOWN_FRAME, f"Unknown frame: {frame}"))

        hidden = get_by_keypath(adv_json, ("display", "hidden")) or False

        if datapack.default_hidden_color and (hidden ^ (color == datapack.default_hidden_color)):
            warnings.append(AdvWarning(AdvWarningType.UNMATCHED_COLOR, "The hidden color does not match the color"))

        if not get_by_keypath(adv_json, ("display", "title", "translate")):
            warnings.append(AdvWarning(AdvWarningType.NO_TRANSLATE, "No 'translate' in title"))

        if not get_by_keypath(adv_json, ("display", "description", "translate")):
            warnings.append(AdvWarning(AdvWarningType.NO_TRANSLATE, "No 'translate' in description"))

        if not get_by_keypath(adv_json, ("parent",)) and not get_by_keypath(adv_json, ("background",)):
            warnings.append(AdvWarning(AdvWarningType.INVALID_PARENT, "No 'parent' or 'background' (for root)"))

        return warnings


class SpellingValidator:
    capitalized: Set[str] = set(json.loads(Path("resources/spelling/capitalized.json").read_text()))

    capitalized_ignore: Set[str] = set(json.loads(Path("resources/spelling/capitalized_ignore.json").read_text()))

    with_the: Set[str] = set(json.loads(Path("resources/spelling/with_the.json").read_text()))

    with_the_ignore: Set[str] = set(json.loads(Path("resources/spelling/with_the_ignore.json").read_text()))

    max_title_length: int = 32

    @classmethod
    def validate_misspelling(cls, adv: Advancement) -> List[AdvWarning]:
        """
        A function for checking basic typos: The name of mobs/measurements with a small letter, etc.
        :param adv: Advancement Class
        :return: List with warnings or None if no misspelling is found.
        """

        warnings = []

        warnings.extend(cls._validate_capitalized(adv.title, "title"))
        warnings.extend(cls._validate_clean_edges(adv.title, "title"))

        warnings.extend(cls._validate_capitalized(adv.description, "description"))
        warnings.extend(cls._validate_the(adv.description, "description"))
        warnings.extend(cls._validate_clean_edges(adv.description, "description"))
        warnings.extend(cls._validate_wrong_symbols_in_fields(adv))
        if not cls._is_valid_title_case(adv.title) and adv.title not in cls.capitalized_ignore:
            warnings.append(AdvWarning(AdvWarningType.MISSPELLING_ERROR,
                                       f"Title \"{adv.title}\" is not written in \"Title Case\", correct variant: \"{titlecase.titlecase(adv.title)}\""))
        return warnings

    @classmethod
    def _validate_capitalized(cls, string: str, place: Literal["title", "description"]) -> List[AdvWarning]:

        warnings = []

        for item_name in chain(ItemProperties.names_list, cls.capitalized_ignore):
            string = string.replace(item_name, '')
        for phrase in cls.capitalized:
            pattern = rf'\b{re.escape(phrase)}\b|\b{re.escape(phrase)}s\b'
            matches = re.finditer(pattern, string, re.IGNORECASE)

            for match in matches:
                original_phrase = match.group()
                start_index, end_index = match.span()

                if original_phrase == phrase.title() or (
                        original_phrase.endswith('s') and original_phrase[:-1] == phrase.title()):
                    continue

                if phrase == "end" and start_index > 0 and string[start_index - 4:start_index].lower() != "the ":
                    continue

                warnings.append(AdvWarning(AdvWarningType.MISSPELLING_ERROR,
                                           f'Phrase "{original_phrase}" at {start_index}:{end_index} should be written in Title Format in {place}'
                                           ))

        return warnings

    @classmethod
    def _validate_the(cls, string: str, place: Literal["title", "description"]) -> List[AdvWarning]:

        lowered_string = string.lower()
        warnings = []

        for ignore_phrase in cls.with_the_ignore:
            lowered_string = lowered_string.replace(ignore_phrase, '')

        for phrase in cls.with_the:
            pattern = rf'\b{re.escape(phrase)}\b'
            matches = re.finditer(pattern, lowered_string)

            for match in matches:
                start_index, end_index = match.span()

                if phrase == "end" and string[start_index:end_index] == "end":
                    continue

                if start_index > 0 and lowered_string[start_index - 4:start_index] == "the ":
                    continue

                warnings.append(AdvWarning(AdvWarningType.MISSPELLING_ERROR,
                                           f'Phrase "{phrase}" at {start_index}:{end_index} should be written with "the" before it in {place}'))

        return warnings

    @classmethod
    def _validate_clean_edges(cls, string: str, place: Literal["title", "description"]) -> List[AdvWarning]:
        warnings = []

        stripped_string = string.strip()

        if string != stripped_string:

            if string.rstrip("\n") != string.rstrip("\n").lstrip():
                warnings.append(AdvWarning(AdvWarningType.MISSPELLING_ERROR, f"{place} has wrong leading spaces"))

            if string.rstrip("\n") != string.rstrip("\n").rstrip():
                warnings.append(AdvWarning(AdvWarningType.MISSPELLING_ERROR, f"{place} has wrong trailing spaces"))

        if stripped_string.endswith(".") and not stripped_string.endswith("..."):
            warnings.append(AdvWarning(AdvWarningType.MISSPELLING_ERROR, f"{place} has wrong dot at the end"))

        return warnings

    @staticmethod
    def _validate_with_pattern(string: str, re_pattern: re.Pattern) -> List[Tuple[int, str]]:
        if re_pattern.match(string):
            return []
        return [(i, char) for i, char in enumerate(string) if not re_pattern.search(char)]

    @classmethod
    def _validate_wrong_symbols_in_fields(cls, adv: Advancement):
        pattern = re.compile(adv.datapack.blacklisted_symbols)
        warnings = []

        fields = {
            "Title": adv.title,
            "Description": adv.description,
        }
        if adv.functions.trophy.item:
            fields["Trophy Name"] = adv.functions.trophy.item.name
            fields["Trophy Lore"] = adv.functions.trophy.item.lore

        for crt in adv.criteria_list:
            fields[f"Criterion {crt.name}"] = crt.name

        for field_name, field_value in fields.items():
            invalid_positions = cls._validate_with_pattern(field_value, pattern)

            if invalid_positions:
                message = (
                    f"'{invalid_positions[0][1]}' at position {invalid_positions[0][0]}"
                    if len(invalid_positions) == 1
                    else ", ".join(f"'{char}' at position {index}" for index, char in invalid_positions)
                )
                warnings.append(AdvWarning(AdvWarningType.WRONG_SYMBOLS, f"Field '{field_name}': {message}"))

        return warnings

    @staticmethod
    def _is_valid_title_case(string: str) -> bool:
        return string.rstrip("\n") == titlecase.titlecase(string.rstrip("\n"))

    @classmethod
    def validate_title(cls, title: str, datapack: Datapack) -> list[AdvWarning]:
        warnings = []

        if len(title) > cls.max_title_length:
            warnings.append(AdvWarning(AdvWarningType.TOO_LONG_TITLE,
                                       f"Title is too long:, max length is {cls.max_title_length} symbols"))

        pattern = re.compile(datapack.blacklisted_symbols)
        if cls._validate_with_pattern(title, pattern):
            warnings.append(AdvWarning(AdvWarningType.WRONG_SYMBOLS, f"Title has blacklisted symbols"))

        warnings.extend(cls._validate_capitalized(title, "title"))

        warnings.extend(cls._validate_clean_edges(title, "title"))

        return warnings
