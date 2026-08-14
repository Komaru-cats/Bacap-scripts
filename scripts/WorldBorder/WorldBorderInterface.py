import shutil
from pathlib import Path

from scripts.WorldBorder.Types import DATAPACK_PRESET_PATH, NoAdvancementReward
from scripts.WorldBorder.WBDataSet import WBDataSet
from scripts.tools import DatapackList
from scripts.tools.Advancement import AdvancementsManager
from scripts.tools.Interface import MenuInterface
from scripts.tools.InterfaceSchema import *
from scripts.tools.utils import fill_pattern

mi = MenuInterface()


class Config:
    pattern_name: str = "WB-Addon-[<version>]"

    dataset = WBDataSet(db_bacap_name="bacap.db", db_bacaped_name="bacaped.db", adv_datapacks=[DatapackList.bacap, DatapackList.default])

    db_targets = ["Bacap", "Bacaped"]


@mi.register_class()
class MI:
    @mi.register_func("Add missing", "a")
    def add_missing(self):
        target = eget_value(
            f"Select a database to add missing [{'/'.join(Config.db_targets)}]:",
            possible_value=Config.db_targets,
        )

        target_datapacks = [DatapackList.bacap] if target == "Bacap" else [DatapackList.bacap, DatapackList.default]

        Config.dataset.add_missing(target, target_datapacks)

    @mi.register_func("Release", "r")
    def release(self) -> None:
        version = eget_value("Version:")
        name = fill_pattern(Config.pattern_name, {"version": version})
        path = Path(f"releases/{name}")
        shutil.copytree(DATAPACK_PRESET_PATH, path, dirs_exist_ok=True)

        version_path = path / "data/bacap_wb_addon/function/config/version.mcfunction"
        version_path.write_text(
            fill_pattern(version_path.read_text(), {"version": version})
        )

        try:
            Config.dataset.generate(datapack_path=path)
        except NoAdvancementReward as e:
            print_warning("Error occurred while generating unified rewards")
            print_warning(e.args[0])
            return

        archive_path = path.with_suffix(".zip")
        if archive_path.exists():
            archive_path.unlink()

        shutil.make_archive(
            base_name=str(path.resolve()), format="zip", root_dir=path, base_dir="."
        )

        shutil.rmtree(path)


AdvancementsManager.generate(force=True)