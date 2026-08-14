import json
from pathlib import Path
from typing import Sequence, Tuple, Optional, Literal

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
    DESC_COLORS,
    FileRewardData,
    REWARD_PATTERN,
    NoAdvancementReward,
    BACAP_TIER_OVERRIDES,
    BACAPED_TIER_OVERRIDES
)


def escape_quotes(string: str) -> str:
    return string.replace('"', '\\"')


class WBDataSet:
    def __init__(
            self, db_bacap_name: str, db_bacaped_name: str, adv_datapacks: Sequence[Datapack]
    ):
        self.adv_datapacks = adv_datapacks

        self.engine_bacap = create_engine(f"sqlite:///wb/{db_bacap_name}")
        Base.metadata.create_all(self.engine_bacap)
        self.session_bacap = sessionmaker(bind=self.engine_bacap)()

        self.engine_bacaped = create_engine(f"sqlite:///wb/{db_bacaped_name}")
        Base.metadata.create_all(self.engine_bacaped)
        self.session_bacaped = sessionmaker(bind=self.engine_bacaped)()

    @staticmethod
    def check_excluded(adv: Advancement):
        adv_path = cut_namespace(adv.mc_path)
        if (
                DATAPACK_PRESET_PATH
                / f"data/bacap_wb_addon/function/rewards/{adv_path}.mcfunction"
        ).exists():
            return True
        return False

    def add_missing(self, target: str, target_datapacks: Sequence[Datapack]):
        for adv in AdvancementsManager.filtered_iterator(datapack=target_datapacks):
            adv: Advancement
            adv_path = cut_namespace(adv.mc_path)
            if self.check_excluded(adv):
                output(f"Skip: {adv.mc_path} as it was excluded")
                continue

            if target == "Bacaped":
                if not self.session_bacaped.query(exists().where(WBSQL.path == adv_path)).scalar():
                    output(f"--- Missing in BACAPED ---")
                    self.set_blocks(adv, self.session_bacaped)

            elif target == "Bacap":
                if not self.session_bacap.query(exists().where(WBSQL.path == adv_path)).scalar():
                    output(f"--- Missing in BACAP ---")
                    cmd_type, blocks = self.set_blocks_return(adv)
                    if blocks > 0 or cmd_type == "set":
                        self.session_bacap.add(
                            WBSQL(
                                path=adv_path,
                                command_type=cmd_type,
                                blocks=blocks,
                            )
                        )
                        self.session_bacap.commit()

    @exit_on_empty_input
    def set_blocks(self, adv: Advancement, session):
        print_adv_data(adv)
        cmd_input = eget_value("Command type [a=add, s=set]:", possible_value=["a", "s"])
        cmd_type = "add" if cmd_input == "a" else "set"

        while True:
            blocks = eget_value("Blocks:", value_type=float)
            # Лимит 21.4 млн работает только для 'add', так как 'set' не умножается на 100
            if cmd_type == "add" and blocks > 21474836:
                print_warning("Limit exceeded! Maximum allowed blocks per 'add' advancement is 21,474,836.")
            else:
                session.add(
                    WBSQL(
                        path=cut_namespace(adv.mc_path),
                        command_type=cmd_type,
                        blocks=blocks,
                    )
                )
                session.commit()
                break

    @exit_on_empty_input
    def set_blocks_return(self, adv: Advancement) -> Tuple[Literal['set', 'add'], float]:
        print_adv_data(adv)
        cmd_input = eget_value("Command type [a=add, s=set]:", possible_value=["a", "s"])
        cmd_type: Literal['set', 'add'] = "set" if cmd_input == "s" else "add"


        while True:
            blocks = eget_value("Blocks:", value_type=float)
            if cmd_type == "add" and blocks > 21474836:
                print_warning("Limit exceeded! Maximum allowed blocks per 'add' advancement is 21,474,836.")
            else:
                return cmd_type, blocks

    def generate(self, datapack_path: Path):
        bacap_init_lines = []
        bacaped_init_lines = []

        for adv in AdvancementsManager.filtered_iterator(datapack=self.adv_datapacks):
            adv: Advancement
            try:
                bacap_line, bacaped_line = self.generate_adv_func_commands(adv, datapack_path)
                if bacap_line:
                    bacap_init_lines.append(bacap_line)
                if bacaped_line:
                    bacaped_init_lines.append(bacaped_line)
            except NoAdvancementReward:
                raise NoAdvancementReward(
                    f"Can't find reward in wb database for adv: {adv.mc_path}, canceled"
                )

        init_blocks_path = datapack_path / "data/bacap_wb_addon/function/init_blocks"
        init_blocks_path.mkdir(parents=True, exist_ok=True)

        if bacap_init_lines:
            (init_blocks_path / "bacap.mcfunction").write_text("\n".join(bacap_init_lines) + "\n", encoding="UTF-8")
        if bacaped_init_lines:
            (init_blocks_path / "bacaped.mcfunction").write_text("\n".join(bacaped_init_lines) + "\n", encoding="UTF-8")

    def generate_adv_func_commands(self, adv: Advancement, datapack_path: Path) -> Tuple[Optional[str], Optional[str]]:
        excluded = False
        data = {}

        adv_path_clean = cut_namespace(adv.mc_path)

        bacap_init_line = None
        bacaped_init_line = None

        if self.check_excluded(adv):
            excluded = True
            in_bacap = True
            in_bacaped = True
        else:
            wb_db_bacap = (
                self.session_bacap.query(WBSQL)
                .filter_by(path=adv_path_clean)
                .first()
            )

            wb_db_bacaped = (
                self.session_bacaped.query(WBSQL)
                .filter_by(path=adv_path_clean)
                .first()
            )

            if not wb_db_bacaped and not wb_db_bacap:
                raise NoAdvancementReward(f"Can't find reward in wb database for {adv.mc_path}")

            color = adv.color.value or adv.datapack.adv_default_type_data[adv.type]["color"]

            # Определяем тип (по умолчанию add)
            cmd_type = "add"
            bacap_blocks = 0

            if wb_db_bacap:
                cmd_type = wb_db_bacap.command_type
                # If SET, take the exact value; if ADD, multiply by 100
                bacap_blocks = int(wb_db_bacap.blocks) if cmd_type == "set" else int(wb_db_bacap.blocks * 100)

            bacaped_blocks = 0
            if wb_db_bacaped:
                cmd_type = wb_db_bacaped.command_type # Can override the type from the base bacap
                bacaped_blocks = int(wb_db_bacaped.blocks) if cmd_type == "set" else int(wb_db_bacaped.blocks * 100)

            in_bacap = wb_db_bacap is not None
            in_bacaped = wb_db_bacaped is not None

            if in_bacap:
                bacap_init_line = f"scoreboard players set {adv.mc_path} wb_adv_blocks {bacap_blocks}"
            if in_bacaped:
                bacaped_init_line = f"scoreboard players set {adv.mc_path} wb_adv_blocks {bacaped_blocks}"

            tier = adv.adv_macro_type

            if in_bacap and adv.mc_path in BACAP_TIER_OVERRIDES:
                tier = BACAP_TIER_OVERRIDES[adv.mc_path]
            elif in_bacaped and adv.mc_path in BACAPED_TIER_OVERRIDES:
                tier = BACAPED_TIER_OVERRIDES[adv.mc_path]

            data = {
                "adv_id": adv.mc_path,
                "adv_title": escape_quotes(adv.title),
                "title_color": color,
                "desc": adv.description.replace('"', r"\"").replace("\n", r"\n"),
                "desc_color": DESC_COLORS[color],
                "tab": adv.datapack.msg_milestone_names[adv.tab]["name"],
                "type": cmd_type,
                "tier": tier
            }

        base_path = Path("data/bacap_wb_addon/function/rewards")
        rel_path = f"{adv_path_clean}.mcfunction"

        reward_file = FileRewardData(
            path=base_path / rel_path if not excluded else None,
            content=fill_pattern(REWARD_PATTERN, data) if not excluded else None,
            excluded=excluded,
        )
        reward_file.write_reward(datapack_path)

        reward_func_path = f"bacap_wb_addon:rewards/{adv_path_clean}"
        tag_content = json.dumps({"values": [reward_func_path]}, indent=2)

        if in_bacap:
            tag_path = datapack_path / f"data/bacap_fanpacks/tags/function/{adv_path_clean}.json"
            tag_path.parent.mkdir(parents=True, exist_ok=True)
            tag_path.write_text(tag_content, encoding="UTF-8")

        if in_bacaped:
            tag_path = datapack_path / f"data/bacaped_fanpacks/tags/function/{adv_path_clean}.json"
            tag_path.parent.mkdir(parents=True, exist_ok=True)
            tag_path.write_text(tag_content, encoding="UTF-8")

        return bacap_init_line, bacaped_init_line