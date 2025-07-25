import json
from dataclasses import dataclass
from pathlib import Path
from typing import Dict

from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import declarative_base

Base = declarative_base()
desc_color_dict: Dict = json.loads(Path("wb/desc_color.json").read_text(encoding="UTF-8"))

DATAPACK_PRESET_PATH = Path("wb/datapack")


class NotAdvRewardFound(KeyError):
    pass


class WBSQL(Base):
    __tablename__ = 'WorldBorder'

    id = Column(Integer, primary_key=True, nullable=False)
    path = Column(String, nullable=False)
    command_type = Column(String, nullable=False)
    blocks = Column(Float, nullable=False)


class RewardPattern:
    vanilla_normal = Path("wb/vanilla_patterns/reward.pattern").read_text(encoding="UTF-8")
    vanilla_fast = Path("wb/vanilla_patterns/fast_reward.pattern").read_text(encoding="UTF-8")
    bukkit_normal = Path("wb/bukkit_patterns/reward.pattern").read_text(encoding="UTF-8")
    bukkit_fast = Path("wb/bukkit_patterns/fast_reward.pattern").read_text(encoding="UTF-8")


@dataclass
class FileRewardData:
    path: Path | None
    content: str | None
    line: str
    excluded: bool

    def write_reward(self, datapack_path: Path):
        if self.excluded:
            return
        path = datapack_path / self.path
        if not path.parent.exists():
            path.parent.mkdir(parents=True)
        path.write_text(self.content, encoding="UTF-8")


@dataclass
class RewardSet:
    normal: FileRewardData
    fast: FileRewardData


@dataclass
class AdvFunctionCommands:
    vanilla: RewardSet
    bukkit: RewardSet

    def write_all_rewards(self, datapack_path: Path):
        self.vanilla.normal.write_reward(datapack_path)
        self.vanilla.fast.write_reward(datapack_path)
        self.bukkit.normal.write_reward(datapack_path)
        self.bukkit.fast.write_reward(datapack_path)
