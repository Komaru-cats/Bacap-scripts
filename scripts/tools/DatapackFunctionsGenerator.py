import json
from collections.abc import Iterable
from pathlib import Path
from typing import List

from .Advancement import AdvancementsManager
from .Datapack import DatapackList, Datapack
from .Patterns import DatapackFunctionsWritePatterns
from .utils import fill_pattern, cut_namespace


class DatapackFunctionsGenerator:
    _bacap_teams: tuple[str, ...] = (
        "aqua", "black", "blue", "dark_aqua", "dark_blue", "dark_gray", "dark_green", "dark_purple", "dark_red", "gold",
        "gray", "green", "light_purple", "red", "white", "yellow")

    @staticmethod
    def _update_function_tag(tag_path: Path, function_mc_path: str, encoding: str = 'utf-8'):

        tag = {
            "replace": False,
            "values": [
                f"{function_mc_path}"
            ]
        }

        tag_path.parent.mkdir(parents=True, exist_ok=True)
        tag_path.write_text(json.dumps(tag, indent=4), encoding=encoding)

    @classmethod
    def generate_update_score(cls, datapack: Datapack | Iterable[Datapack]):

        datapack = datapack if isinstance(datapack, Iterable) else (datapack,)

        for dp in datapack:

            dp_update_score_path = dp.reward_path / "update_score.mcfunction"

            dp_update_score = ""

            adv_mc_paths = sorted(
                set(adv.mc_path for adv in AdvancementsManager.filtered_iterator(datapack=dp) if not adv.hidden))

            for mc_path in adv_mc_paths:
                dp_update_score += f"{fill_pattern(DatapackFunctionsWritePatterns.update_score, {"adv_path_in_mc": mc_path})}\n"

            cls._update_function_tag(
                tag_path=dp.path / f"data/{DatapackList.bacap.fanpacks_namespace}/tags/function/update_score.json",
                function_mc_path=f"{dp.reward_namespace}:update_score", encoding=dp.encoding)

            dp_update_score_path.write_text(dp_update_score, encoding=dp.encoding)

    @classmethod
    def generate_coop_update(cls, datapack: Datapack | Iterable[Datapack]):

        datapack = datapack if isinstance(datapack, Iterable) else (datapack,)

        for dp in datapack:

            dp_coop_update_path = dp.function_path / "config" / "coop_update.mcfunction"

            adv_mc_paths = sorted(set(adv.mc_path for adv in AdvancementsManager.filtered_iterator(datapack=dp)))

            dp_coop_update = ''

            for mc_path in adv_mc_paths:
                dp_coop_update += f"{fill_pattern(DatapackFunctionsWritePatterns.coop_update, {"adv_path_in_mc": mc_path})}\n"

            cls._update_function_tag(
                tag_path=dp.path / f"data/{DatapackList.bacap.fanpacks_namespace}/tags/function/config/coop_update.json",
                function_mc_path=f"{dp.default_adv_namespace}:config/coop_update", encoding=dp.encoding)
            dp_coop_update_path.write_text(dp_coop_update, encoding=dp.encoding)

    @classmethod
    def generate_coop_update_team(cls, datapack: Datapack | Iterable[Datapack]):

        datapack = datapack if isinstance(datapack, Iterable) else (datapack,)

        for dp in datapack:
            for color in cls._bacap_teams:
                dp_coop_update_team_path = dp.function_path / f"config/coop_update_team_{color}.mcfunction"

                dp_coop_update_team = ''

                adv_mc_paths = sorted(set(adv.mc_path for adv in AdvancementsManager.filtered_iterator(datapack=dp)))

                for mc_path in adv_mc_paths:
                    dp_coop_update_team += f"{fill_pattern(DatapackFunctionsWritePatterns.coop_update_team, {"adv_path_in_mc": mc_path, "color_team": color})}\n"

                cls._update_function_tag(
                    tag_path=dp.path / f"data/{DatapackList.bacap.fanpacks_namespace}/tags/function/config/coop_update_team_{color}.json",
                    function_mc_path=f"{dp.default_adv_namespace}:config/coop_update_team_{color}",
                    encoding=dp.encoding)
                dp_coop_update_team_path.write_text(dp_coop_update_team, encoding=dp.encoding)

    @classmethod
    def generate_grant_trophies(cls, datapack: Datapack | Iterable[Datapack]):

        datapack = datapack if isinstance(datapack, Iterable) else (datapack,)

        for dp in datapack:
            adv_with_trophies_data = [adv for adv in AdvancementsManager.deep_find(
                {"functions": lambda functions: bool(functions.trophy.item)}, datapack=dp)]
            adv_with_trophies_data.sort()

            dp_grant_trophies_path = dp.function_path / "config/grant_trophies.mcfunction"

            dp_grant_trophies = ''

            for adv in adv_with_trophies_data:
                dp_grant_trophies += f"{fill_pattern(DatapackFunctionsWritePatterns.grant_trophies,
                                                     {"adv_path_in_mc": adv.mc_path, "internal_name": adv.reward_mcpath,
                                                      "reward_namespace": adv.datapack.reward_namespace, "reward_path": cut_namespace(adv.reward_mcpath)})}\n"

            cls._update_function_tag(
                tag_path=dp.path / f"data/{DatapackList.bacap.fanpacks_namespace}/tags/function/config/grant_trophies.json",
                function_mc_path=f"{dp.default_adv_namespace}:config/grant_trophies", encoding=dp.encoding)

            dp_grant_trophies_path.write_text(dp_grant_trophies, encoding=dp.encoding)

    @classmethod
    def generate_all(cls, datapack: Datapack | List[Datapack]):
        """
        Generates all functions for datapack (update_score, coop_update, coop_team_update, grant_trophies)
        """
        cls.generate_update_score(datapack)
        cls.generate_coop_update(datapack)
        cls.generate_coop_update_team(datapack)
        cls.generate_grant_trophies(datapack)
