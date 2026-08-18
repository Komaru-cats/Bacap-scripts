import json
from dataclasses import dataclass
from pathlib import Path
from typing import Literal

from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import declarative_base

Base = declarative_base()

DESC_COLORS: dict = json.loads(Path("wb/desc_color.json").read_text(encoding="UTF-8"))
DATAPACK_PRESET_PATH = Path("wb/datapack")

REWARD_PATTERN = Path("wb/patterns/reward.txt").read_text(encoding="UTF-8")
CUSTOM_TIER_BLOCKS_REWARD_PATTERN = Path("wb/patterns/custom_tier_blocks_reward_pattern.txt").read_text(encoding="UTF-8")

class NoAdvancementReward(KeyError):
    pass

class IndividualBlock(Base):
    __tablename__ = "individual_blocks"
    id = Column(Integer, primary_key=True, autoincrement=True)
    path = Column(String, nullable=False, unique=True)
    command_type: Literal['set', 'add'] = Column(String, nullable=False)  # 'add' or 'set'
    blocks_bacap = Column(Float, nullable=True)
    blocks_bacaped = Column(Float, nullable=True)

class TierCustomBlock(Base):
    __tablename__ = "tier_custom_blocks"
    mc_path = Column(String, primary_key=True, nullable=False)
    bacap = Column(Float, nullable=True)
    bacaped = Column(Float, nullable=True)

class TierOverride(Base):
    __tablename__ = "tier_overrides"
    mc_path = Column(String, primary_key=True, nullable=False)
    bacap = Column(String, nullable=True)
    bacaped = Column(String, nullable=True)

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