import shutil
from pathlib import Path

from scripts.WorldBorder.Types import DATAPACK_PRESET_PATH, NotAdvRewardFound
from scripts.WorldBorder.WBDataSet import WBDataSet
from scripts.tools import DatapackList
from scripts.tools.Advancement import AdvancementsManager
from scripts.tools.Interface import MenuInterface
from scripts.tools.InterfaceSchema import *
from scripts.tools.utils import fill_pattern

mi = MenuInterface()


class Config:
    pattern_name: str = "WB-Addon-[<version>]"
    types = {
        "Bacap": WBDataSet("bacap.db", [DatapackList.bacap], "bacap"),
        "Bacaped": WBDataSet("bacaped.db", [DatapackList.bacap, DatapackList.default], "bacaped")
    }


@mi.register_class()
class MI:
    @mi.register_func("Add missing", "a")
    def add_missing(self):
        datapack_set = Config.types[
            eget_value(f"Select a datapack set [{"/".join(Config.types.keys())}]:", possible_value=Config.types.keys())]
        datapack_set.add_missing()

    @mi.register_func("Release", "r")
    def release(self) -> None:
        version = eget_value("Version:")
        name = fill_pattern(Config.pattern_name, {"version": version})
        path = Path(f"releases/{name}")
        shutil.copytree(DATAPACK_PRESET_PATH, path, dirs_exist_ok=True)

        version_path = path / "data/bc_wb/function/version.mcfunction"
        version_path.write_text(fill_pattern(version_path.read_text(), {"version": version}))

        for d_name, d_set in Config.types.items():
            try:
                d_set.generate(datapack_path=path)
            except NotAdvRewardFound as e:
                print_warning(f"Error occurred while generating {d_name}")
                print_warning(e.args[0])
                return

        # Удаляем архив, если он уже существует ИНАЧЕ ПИЗДЕЦ
        archive_path = path.with_suffix(".zip")
        if archive_path.exists():
            archive_path.unlink()

        shutil.make_archive(
            base_name=str(path.resolve()),
            format="zip",
            root_dir=path,
            base_dir='.'
        )

        shutil.rmtree(path)


AdvancementsManager.generate(force=True)
