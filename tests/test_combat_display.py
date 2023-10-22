from watercrest.entity.character import (
    Character,
    CharacterClass,
    CharacterLevel,
    CharacterStatistics,
)
from watercrest.entity.weapon import (
    WeaponCategory,
    WeaponInfo,
    WeaponRank,
)
from watercrest.service.combat_service import CombatService


def test_sample_combat():
    spam = Character(
        name="spam",
        character_class=CharacterClass.BRIGAND,
        character_level=CharacterLevel(),
        character_statistics=CharacterStatistics(
            health_points=18,
            strength=4,
            skill=8,
            speed=8,
            luck=0,
            defense=4,
            resistance=0,
            constitution=9,
            movement=5,
            axe_proficiency=WeaponRank.D,
        ),
        weapon_equip=WeaponInfo(
            name="iron axe",
            weapon_category=WeaponCategory.AXE,
            rank=WeaponRank.E,
            uses=45,
            might=8,
            hit=80,
            crit=0,
            range=1,
            weight=10,
        ),
    )
    ham = Character(
        name="ham",
        character_class=CharacterClass.MERCENARY,
        character_level=CharacterLevel(),
        character_statistics=CharacterStatistics(
            health_points=18,
            strength=4,
            skill=8,
            speed=8,
            luck=0,
            defense=4,
            resistance=0,
            constitution=9,
            movement=5,
            sword_proficiency=WeaponRank.D,
        ),
        weapon_equip=WeaponInfo(
            name="iron sword",
            weapon_category=WeaponCategory.SWORD,
            rank=WeaponRank.E,
            uses=46,
            might=6,
            hit=95,
            crit=0,
            range=1,
            weight=5,
        ),
    )

    combat_service = CombatService()
    combat_display_info = combat_service.display_combat_info(spam, ham)
    print(combat_display_info)
    assert combat_display_info["attacker_crit"] >= 0  # Crit should always be positive
    assert combat_display_info["defender_crit"] >= 0  # Crit should always be positive
