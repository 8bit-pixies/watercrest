from typing import Dict, Optional
from watercrest.entity.weapon import WeaponInfo, WeaponTriangle
from watercrest.entity.weapon import WeaponCategory


class WeaponTriangleService:
    def __init__(self):
        self.weapon_triangle_mapping: Dict[WeaponTriangle, int] = {
            WeaponTriangle.WINNING: 1,
            WeaponTriangle.LOSING: -1,
            WeaponTriangle.NEUTRAL: 0,
        }

    def weapon_triangle_outcome(
        self,
        attacker_weapon_info: Optional[WeaponInfo],
        defender_weapon_info: Optional[WeaponInfo],
        as_indicator: bool = False,
    ):
        attacker_weapon = attacker_weapon_info.weapon_category
        defender_weapon = defender_weapon_info.weapon_category
        is_weapon_triangle_reversal = (
            attacker_weapon_info.is_weapon_triangle_reversal or defender_weapon_info.is_weapon_triangle_reversal
        )
        outcome: WeaponTriangle = WeaponTriangle.NEUTRAL
        if defender_weapon is None or attacker_weapon is None:
            outcome: WeaponTriangle = WeaponTriangle.NEUTRAL
        elif (
            attacker_weapon in [WeaponCategory.BOW, WeaponCategory.OTHER]
            or defender_weapon in [WeaponCategory.BOW, WeaponCategory.OTHER]
            or attacker_weapon == defender_weapon
        ):
            outcome: WeaponTriangle = WeaponTriangle.NEUTRAL
        elif attacker_weapon == WeaponCategory.AXE and defender_weapon == WeaponCategory.LANCE:
            outcome: WeaponTriangle = WeaponTriangle.WINNING
        elif attacker_weapon == WeaponCategory.SWORD and defender_weapon == WeaponCategory.AXE:
            outcome: WeaponTriangle = WeaponTriangle.WINNING
        elif attacker_weapon == WeaponCategory.LANCE and defender_weapon == WeaponCategory.SWORD:
            outcome: WeaponTriangle = WeaponTriangle.WINNING
        else:
            outcome: WeaponTriangle = WeaponTriangle.LOSING

        if is_weapon_triangle_reversal and outcome == WeaponTriangle.LOSING:
            outcome = WeaponTriangle.WINNING
        elif is_weapon_triangle_reversal and outcome == WeaponTriangle.WINNING:
            outcome = WeaponTriangle.LOSING

        if as_indicator:
            return self.weapon_triangle_mapping[outcome]
        else:
            return outcome
