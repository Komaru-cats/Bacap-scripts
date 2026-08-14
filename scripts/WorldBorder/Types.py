import json
from dataclasses import dataclass
from pathlib import Path
from typing import Literal

from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import declarative_base

Base = declarative_base()
DESC_COLORS: dict = json.loads(
    Path("wb/desc_color.json").read_text(encoding="UTF-8")
)
BACAP_TIER_OVERRIDES: dict = json.loads(
    Path("wb/bacap_tier_overrides.json").read_text(encoding="UTF-8")
)

BACAPED_TIER_OVERRIDES: dict = json.loads(
    Path("wb/bacaped_tier_overrides.json").read_text(encoding="UTF-8")
)

DATAPACK_PRESET_PATH = Path("wb/datapack")

class NoAdvancementReward(KeyError):
    pass

class WBSQL(Base):
    __tablename__ = "WorldBorder"

    id = Column(Integer, primary_key=True, nullable=False)
    path = Column(String, nullable=False)
    command_type: Literal['add', 'set'] = Column(String, nullable=False)
    blocks = Column(Float, nullable=False)

REWARD_PATTERN = Path("wb/patterns/reward.pattern").read_text(encoding="UTF-8")

@dataclass
class FileRewardData:
    path: Path | None
    content: str | None
    excluded: bool

    def write_reward(self, datapack_path: Path):
        if self.excluded or not self.path:
            return
        full_path = datapack_path / self.path
        full_path.parent.mkdir(parents=True, exist_ok=True)
        full_path.write_text(self.content, encoding="UTF-8")