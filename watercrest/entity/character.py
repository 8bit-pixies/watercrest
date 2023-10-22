from typing import List, Optional
from pydantic import BaseModel

from watercrest.entity.weapon import WeaponInfo, WeaponRank


from watercrest.entity.character_class import CharacterClass


class CharacterLevel(BaseModel):
    level: int = 1
    experience: int = 0


class CharacterStatistics(BaseModel):
    health_points: float = 10
    strength: float = 0
    magic: float = 0  # not used yet
    skill: float = 0
    speed: float = 0
    luck: float = 0
    defense: float = 0
    resistance: float = 0
    constitution: float = 0
    movement: float = 5
    axe_proficiency: Optional[WeaponRank] = None
    bow_proficiency: Optional[WeaponRank] = None
    lance_proficiency: Optional[WeaponRank] = None
    sword_proficiency: Optional[WeaponRank] = None


class Character(BaseModel):
    name: str
    character_class: CharacterClass
    character_level: CharacterLevel
    character_statistics: CharacterStatistics
    weapon_equip: WeaponInfo
    items: List[WeaponInfo] = []

