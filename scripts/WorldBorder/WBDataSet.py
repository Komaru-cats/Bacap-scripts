from pathlib import Path
from typing import Sequence

from sqlalchemy import create_engine, exists
from sqlalchemy.orm import sessionmaker

from scripts.tools.Advancement import AdvancementsManager
from scripts.tools.Datapack import Datapack
from scripts.tools.Interface import exit_on_empty_input
from scripts.tools.InterfaceSchema import *
from scripts.tools.utils import cut_namespace, fill_pattern
from .Types import (
    DATAPACK_PRESET_PATH,
    Base,
    WBSQL,
    desc_color_dict,
    FileRewardData,
    RewardPattern,
    NotAdvRewardFound,
    AdvFunctionCommands,
)


def time_formula(x: float):
    if x < 0:
        raise ValueError("Time must be positive")
    if x == 0:
        return 1
    return max(1, int((x / x**0.6 * 2) * 20))


def escape_quotes(string: str) -> str:
    return string.replace('"', '\\"')


class WBDataSet:
    def __init__(
        self, db_name: str, adv_datapacks: Sequence[Datapack], reward_folder_name: str
    ):
        self.adv_datapacks = adv_datapacks
        self.reward_folder_name = reward_folder_name
        self.engine = create_engine(f"sqlite:///wb/{db_name}")
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

    def check_excluded(self, adv: Advancement):
        """
        This check is needed because some advancements are excluded from the wb
        Checking path without 'vanilla' subdivision now.
        """
        adv_path = cut_namespace(adv.mc_path)
        if (
            DATAPACK_PRESET_PATH
            / f"data/bc_wb/function/rewards/{self.reward_folder_name}/normal/{adv_path}.mcfunction"
        ).exists():
            return True
        return False

    def add_missing(self):
        for adv in AdvancementsManager.filtered_iterator(datapack=self.adv_datapacks):
            adv_path = cut_namespace(adv.mc_path)
            if self.check_excluded(adv):
                output(f"Skip: {adv.mc_path} as it was excluded")
                continue
            if not self.session.query(exists().where(WBSQL.path == adv_path)).scalar():
                self.set_blocks(adv)

    @exit_on_empty_input
    def set_blocks(self, adv: Advancement):
        print_adv_data(adv)
        self.session.add(
            WBSQL(
                path=cut_namespace(adv.mc_path),
                command_type="add",
                blocks=eget_value("Blocks:", value_type=float),
            )
        )
        self.session.commit()

    def generate(self, datapack_path: Path):
        """
        If all advancements are found, it will generate the data into `datapack_path` for every advancement in DataSet.
        """
        advFC_list: list[AdvFunctionCommands] = []
        for adv in AdvancementsManager.filtered_iterator(datapack=self.adv_datapacks):
            try:
                advFC_list.append(self.generate_adv_func_commands(adv))
            except NotAdvRewardFound:
                raise NotAdvRewardFound(
                    f"Can't find reward in wb database for adv: {adv.mc_path}, canceled"
                )

        normal_lines = ""
        fast_lines = ""

        for advFC in advFC_list:
            normal_lines += advFC.normal.line + "\n"
            fast_lines += advFC.fast.line + "\n"
            advFC.write_all_rewards(datapack_path)

        path_to_checkers = (
            datapack_path
            / f"data/bc_wb/function/complete_checkers/{self.reward_folder_name}"
        )
        checkers = [
            ("normal.mcfunction", normal_lines),
            ("fast.mcfunction", fast_lines),
        ]

        for relative_path, content in checkers:
            full_path = path_to_checkers / relative_path
            full_path.parent.mkdir(parents=True, exist_ok=True)
            full_path.write_text(content, encoding="UTF-8")

    def generate_adv_func_commands(self, adv: Advancement) -> AdvFunctionCommands:
        """
        This function is used to generate the adv_func_commands for one advancement.
        """
        excluded = False
        data = {}

        if self.check_excluded(adv):
            excluded = True
            # Для исключенных используем путь из самого достижения
            reward_path_base = cut_namespace(adv.mc_path)
        else:
            wb_db = (
                self.session.query(WBSQL)
                .filter_by(path=cut_namespace(adv.mc_path))
                .first()
            )
            if not wb_db:
                raise NotAdvRewardFound("Can't find reward in wb database")

            reward_path_base = wb_db.path

            color = (
                adv.color.value or adv.datapack.adv_default_type_data[adv.type]["color"]
            )
            data = {
                "blocks": str(wb_db.blocks),
                "time": str(time_formula(wb_db.blocks)),
                "blocks_d2": str(wb_db.blocks / 2),
                "title": escape_quotes(adv.title),
                "description": adv.description.replace('"', r"\"").replace("\n", r"\n"),
                "color": color,
                "tab": adv.datapack.msg_milestone_names[adv.tab]["name"],
                "desc_color": desc_color_dict[color],
                "adv_mc_path": adv.mc_path,
            }

        base_path = Path(f"data/bc_wb/function/rewards/{self.reward_folder_name}")

        line_pattern = (
            f"execute if score [<adv_mc_path>] bac_obtained matches 1.. "
            f"unless score [<adv_mc_path>] wb matches 1 "
            f"if score is_wb_run wb matches 1 "
            f"run function bc_wb:rewards/{self.reward_folder_name}/[<reward_path>]"
        )

        # Normal
        normal_rel_path = f"normal/{cut_namespace(adv.mc_path)}.mcfunction"
        normal = FileRewardData(
            path=base_path / normal_rel_path if not excluded else None,
            content=fill_pattern(RewardPattern.normal, data) if not excluded else None,
            line=fill_pattern(
                line_pattern,
                {
                    "adv_mc_path": adv.mc_path,
                    "reward_path": f"normal/{reward_path_base}",
                },
            ),
            excluded=excluded,
        )

        # Fast
        fast_rel_path = f"fast/{cut_namespace(adv.mc_path)}.mcfunction"
        fast = FileRewardData(
            path=base_path / fast_rel_path if not excluded else None,
            content=fill_pattern(RewardPattern.fast, data) if not excluded else None,
            line=fill_pattern(
                line_pattern,
                {
                    "adv_mc_path": adv.mc_path,
                    "reward_path": f"fast/{reward_path_base}",
                },
            ),
            excluded=excluded,
        )

        return AdvFunctionCommands(normal, fast)
