from typing import List, Optional
from pydantic import BaseModel
from enum import Enum
from pathlib import Path
import warnings
import tomli

from watercrest.entity.character_class import CharacterClass


class WeaponCategory(str, Enum):
    AXE = "AXE"
    BOW = "BOW"
    LANCE = "LANCE"
    SWORD = "SWORD"
    OTHER = "OTHER"


class WeaponRank(str, Enum):
    S = "S"
    A = "A"
    B = "B"
    C = "C"
    D = "D"
    E = "E"


class WeaponInfo(BaseModel):
    name: str = ""
    weapon_category: WeaponCategory = WeaponCategory("OTHER")
    rank: WeaponRank = WeaponRank("E")  # Don't support unique weapons yet
    uses: int = 1
    might: int = 1
    hit: int = 1
    crit: int = 1
    range: int = 1
    weight: int = 1
    character_class_restriction: Optional[List[CharacterClass]] = None
    character_name_restriction: Optional[List[str]] = None
    is_weapon_triangle_reversal: bool = False

    # add model validator to load the class to weapon mapping - then can remove the calss
    # restriction field, as it should be declared differently.

    @classmethod
    def from_config(cls, name, config_override: dict = {}, config_delta: dict = {}):
        weapons = tomli.load(open(Path(__file__).parent.joinpath("resources/weapon.toml"), "rb"))
        if name not in weapons:
            raise ValueError(f"Weapon: {name} - is not found in the database.")
        weapon = weapons[name]
        for key, value in config_override.items():
            weapon[key] = value
        for key, value in config_delta.items():
            if key in config_override:
                warnings.warn(f"Key: {key} - is found in config override and will not be applied as a delta")
                continue
            else:
                weapon[key] = weapon[key] + value
        return cls.model_validate(weapon)


class WeaponTriangle(str, Enum):
    WINNING = "WINNING"
    LOSING = "LOSING"
    NEUTRAL = "NEUTRAL"
