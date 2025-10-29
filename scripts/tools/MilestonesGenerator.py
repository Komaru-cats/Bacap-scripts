import json
from collections.abc import Iterable

from . import Datapack, AdvancementsManager
from .utils import get_adv_json


class MilestonesGenerator:

    @staticmethod
    def generate_milestones(datapack: Datapack | Iterable[Datapack]) -> None:

        datapack = datapack if isinstance(datapack, Iterable) else (datapack,)

        for dp in datapack:
            if not dp.milestone_advs_path:
                continue
            adv_by_tab_no_hidden = AdvancementsManager.split_by_tabs(
                [adv for adv in AdvancementsManager.filtered_iterator(datapack=dp) if not adv.hidden]
            )

            for tab, milestone_path in dp.milestone_advs_path.items():
                adv_json = get_adv_json(milestone_path)

                adv_json["criteria"] = {}

                for adv in adv_by_tab_no_hidden.get(tab, []):
                    criteria = {
                        "trigger": "minecraft:location",
                        "conditions": {
                            "player": {
                                "type_specific": {
                                    "type": "player",
                                    "advancements": {}
                                }
                            }
                        }
                    }
                    criteria["conditions"]["player"]["type_specific"]["advancements"][adv.mc_path] = True
                    adv_json["criteria"][adv.filename] = criteria

                milestone_path.write_text(json.dumps(adv_json, indent=2), encoding=dp.encoding)
                AdvancementsManager.update_advancement(milestone_path, dp)

    @staticmethod
    def generate_advancement_legend(datapack: Datapack | Iterable[Datapack]):

        datapack = datapack if isinstance(datapack, Iterable) else (datapack,)

        for dp in datapack:

            if not dp.legend_adv_mcpath:
                continue

            adv_json = get_adv_json(dp.legend_adv_path)
            adv_list_no_hidden = [adv for adv in AdvancementsManager.filtered_list(datapack=dp) if not adv.hidden]
            adv_json["criteria"] = {}

            for adv in adv_list_no_hidden:

                if adv.path == dp.legend_adv_path:
                    continue

                criteria = {"trigger": "minecraft:location",
                            "conditions": {"player": {"type_specific": {"type": "player", "advancements": {}}}}}
                criteria["conditions"]["player"]["type_specific"]["advancements"][adv.mc_path] = True
                adv_json["criteria"][adv.filename] = criteria

            dp.legend_adv_path.write_text(json.dumps(adv_json, indent=2), encoding=dp.encoding)

            AdvancementsManager.update_advancement(dp.legend_adv_path, dp)

    @classmethod
    def generate_all(cls, datapack: Datapack | Iterable[Datapack]) -> None:
        cls.generate_milestones(datapack)
        cls.generate_advancement_legend(datapack)
