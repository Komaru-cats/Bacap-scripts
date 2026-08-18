import json
from pathlib import Path
from typing import Sequence, Tuple, Optional, Literal

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from scripts.tools.Advancement import AdvancementsManager
from scripts.tools.Datapack import Datapack
from scripts.tools.Interface import exit_on_empty_input
from scripts.tools.InterfaceSchema import print_adv_data, eget_value, print_warning, output
from scripts.tools.utils import cut_namespace, fill_pattern
from tools import Advancement

from .Types import (
    DATAPACK_PRESET_PATH,
    Base,
    IndividualBlock,
    TierCustomBlock,
    TierOverride,
    DESC_COLORS,
    FileRewardData,
    REWARD_PATTERN,
    CUSTOM_TIER_BLOCKS_REWARD_PATTERN,
    NoAdvancementReward
)


def escape_quotes(string: str) -> str:
    return string.replace('"', '\\"')


class WBDataSet:
    def __init__(self, db_name: str, adv_datapacks: Sequence[Datapack]):
        self.adv_datapacks = adv_datapacks
        self.engine = create_engine(f"sqlite:///wb/{db_name}")
        Base.metadata.create_all(self.engine)
        self.session = sessionmaker(bind=self.engine)()

    @staticmethod
    def check_excluded(adv) -> bool:
        adv_path = cut_namespace(adv.mc_path)
        func_path = DATAPACK_PRESET_PATH / f"data/bacap_wb_addon/function/rewards/{adv_path}.mcfunction"
        return func_path.exists()

    def add_missing(self, target: Literal["Bacap", "Bacaped"], target_datapacks: Sequence[Datapack]):
        for adv in AdvancementsManager.filtered_iterator(datapack=target_datapacks):

            if self.check_excluded(adv):
                output(f"Skip: {adv.mc_path} (Excluded)")
                continue

            record = self.session.query(IndividualBlock).filter_by(path=adv.mc_path).first()
            is_missing = False

            if target == "Bacap" and (not record or record.blocks_bacap is None):
                is_missing = True
            elif target == "Bacaped" and (not record or record.blocks_bacaped is None):
                is_missing = True

            if is_missing:
                output(f"--- Missing in {target.upper()} ---")
                self._prompt_and_save_blocks(adv, target, record)  # убрали adv_path из аргументов

    @exit_on_empty_input
    def _prompt_and_save_blocks(self, adv: Advancement, target: str, record: Optional[IndividualBlock]):
        print_adv_data(adv)

        cmd_type = record.command_type if record else None
        if not cmd_type:
            cmd_input = eget_value("Command type [a=add, s=set]:", possible_value=["a", "s"])
            cmd_type = "add" if cmd_input == "a" else "set"

        while True:
            blocks = eget_value("Blocks:", value_type=float)
            if cmd_type == "add" and blocks > 21474836:
                print_warning("Limit exceeded!")
                continue

            if not record:
                record = IndividualBlock(path=adv.mc_path, command_type=cmd_type)
                self.session.add(record)

            if target == "Bacap":
                record.blocks_bacap = blocks
            else:
                record.blocks_bacaped = blocks

            self.session.commit()
            break

    def generate(self, datapack_path: Path):
        bacap_init_lines, bacaped_init_lines = [], []

        for adv in AdvancementsManager.filtered_iterator(datapack=self.adv_datapacks):
            try:
                b_line, bed_line = self.generate_adv_func_commands(adv, datapack_path)
                if b_line: bacap_init_lines.append(b_line)
                if bed_line: bacaped_init_lines.append(bed_line)
            except NoAdvancementReward as e:
                raise NoAdvancementReward(f"Can't find reward for {adv.mc_path} | {e}")

        init_path = datapack_path / "data/bacap_wb_addon/function/init_blocks"
        init_path.mkdir(parents=True, exist_ok=True)

        if bacap_init_lines:
            (init_path / "bacap.mcfunction").write_text("\n".join(bacap_init_lines) + "\n", encoding="UTF-8")
        if bacaped_init_lines:
            (init_path / "bacaped.mcfunction").write_text("\n".join(bacaped_init_lines) + "\n", encoding="UTF-8")

    @staticmethod
    def _calc_blocks(raw_blocks: float, cmd_type: str) -> int:
        return int(raw_blocks) if cmd_type == "set" else int(raw_blocks * 100)


    def generate_adv_func_commands(self, adv: Advancement, datapack_path: Path) -> Tuple[Optional[str], Optional[str]]:
        adv_path_clean = cut_namespace(adv.mc_path)
        excluded = self.check_excluded(adv)

        ind_block, t_custom, t_over = self._fetch_db_records(adv.mc_path)

        in_bacap, in_bacaped = self._check_availability(ind_block, excluded)
        if not in_bacap and not in_bacaped:
            raise NoAdvancementReward("Not in DB")

        cmd_type = ind_block.command_type if ind_block else "add"

        bacap_init, bacaped_init, tier, custom_blocks = self._calculate_init_lines_and_tiers(
            adv, ind_block, t_custom, t_over, cmd_type, in_bacap, in_bacaped, excluded
        )

        self._generate_and_write_reward(
            adv, adv_path_clean, datapack_path, cmd_type, tier, custom_blocks, excluded
        )

        self._write_function_tags(adv_path_clean, datapack_path, in_bacap, in_bacaped)

        return bacap_init, bacaped_init


    def _fetch_db_records(self, mc_path: str):
        """Извлекает все необходимые записи из базы данных."""
        ind_block = self.session.query(IndividualBlock).filter_by(path=mc_path).first()
        t_custom = self.session.query(TierCustomBlock).filter_by(mc_path=mc_path).first()
        t_over = self.session.query(TierOverride).filter_by(mc_path=mc_path).first()
        return ind_block, t_custom, t_over

    @staticmethod
    def _check_availability(ind_block, excluded: bool) -> Tuple[bool, bool]:
        in_bacap = (ind_block and ind_block.blocks_bacap is not None) or excluded
        in_bacaped = (ind_block and ind_block.blocks_bacaped is not None) or excluded
        return in_bacap, in_bacaped

    def _calculate_init_lines_and_tiers(self, adv, ind_block, t_custom, t_over, cmd_type, in_bacap, in_bacaped, excluded):
        bacap_init_line, bacaped_init_line = None, None
        tier = adv.adv_macro_type
        custom_blocks_value = None

        if in_bacap and not excluded:
            blocks = self._calc_blocks(ind_block.blocks_bacap, cmd_type)
            bacap_init_line = f"scoreboard players set {adv.mc_path} wb_adv_blocks {blocks}"
            if t_over and t_over.bacap:
                tier = t_over.bacap
            if t_custom and t_custom.bacap:
                tier, custom_blocks_value = "custom", int(t_custom.bacap * 100)

        if in_bacaped and not excluded:
            blocks = self._calc_blocks(ind_block.blocks_bacaped, cmd_type)
            bacaped_init_line = f"scoreboard players set {adv.mc_path} wb_adv_blocks {blocks}"
            if t_over and t_over.bacaped:
                tier = t_over.bacaped
            if t_custom and t_custom.bacaped:
                tier, custom_blocks_value = "custom", int(t_custom.bacaped * 100)

        return bacap_init_line, bacaped_init_line, tier, custom_blocks_value

    @staticmethod
    def _generate_and_write_reward(adv: Advancement, adv_path_clean: str, datapack_path: Path, cmd_type: str, tier: str, custom_blocks_value: Optional[int], excluded: bool) -> None:
        color = adv.color.value or adv.datapack.adv_default_type_data[adv.type]["color"]
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

        if custom_blocks_value is not None:
            data["custom_tier_blocks"] = str(custom_blocks_value)

        active_pattern = CUSTOM_TIER_BLOCKS_REWARD_PATTERN if tier == "custom" else REWARD_PATTERN
        rel_path = f"data/bacap_wb_addon/function/rewards/{adv_path_clean}.mcfunction"

        reward_file = FileRewardData(
            path=Path(rel_path) if not excluded else None,
            content=fill_pattern(active_pattern, data) if not excluded else None,
            excluded=excluded,
        )
        reward_file.write_reward(datapack_path)

    def _write_function_tags(self, adv_path_clean: str, datapack_path: Path, in_bacap: bool, in_bacaped: bool) -> None:
        tag_content = json.dumps({"values": [f"bacap_wb_addon:rewards/{adv_path_clean}"]}, indent=2)

        if in_bacap:
            self._write_json_file(datapack_path / f"data/bacap_fanpacks/tags/function/{adv_path_clean}.json", tag_content)

        if in_bacaped:
            self._write_json_file(datapack_path / f"data/bacaped_fanpacks/tags/function/{adv_path_clean}.json", tag_content)

    @staticmethod
    def _write_json_file(path: Path, content: str) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="UTF-8")