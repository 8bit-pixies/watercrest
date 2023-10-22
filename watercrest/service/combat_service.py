from watercrest.entity.character import Character
from watercrest.service.weapon_triangle_service import WeaponTriangleService

from watercrest.utils.distribution_util import DistributionUtil


class CombatService:
    def __init__(self):
        self.triangle_attack_value = 2
        self.triangle_hit_value = 15
        self.attack_speed_double_hit_threshold = 4

    def get_weapon_triangle_bonus(self, attacker_character: Character, defender_character: Character):
        weapon_triangle_indicator = WeaponTriangleService().weapon_triangle_outcome(
            attacker_character.weapon_equip, defender_character.weapon_equip, as_indicator=True
        )
        return {
            "triangle_attack_value": self.triangle_attack_value * weapon_triangle_indicator,
            "triangle_hit_value": self.triangle_hit_value * weapon_triangle_indicator,
        }

    def get_attack_damage(self, character: Character, attack_triangle: float, attack_support: int = 0):
        attack = character.character_statistics.strength
        effectiveness = 1
        weapon_might = character.weapon_equip.might
        if attack_triangle > 0:
            effectiveness = 3
        attack_damage = attack + effectiveness * (weapon_might + attack_triangle) + attack_support
        return attack_damage

    def get_attack_info(self, attacker_character: Character, defender_character: Character):
        weapon_triangle_bonus = self.get_weapon_triangle_bonus(attacker_character, defender_character)
        attacker_damage = self.get_attack_damage(
            attacker_character, float(weapon_triangle_bonus.get("triangle_attack_value", 0))
        )
        defender_damage = self.get_attack_damage(
            defender_character, float(weapon_triangle_bonus.get("triangle_attack_value", 0)) * -1.0
        )
        attack_info = {
            "attacker_damage": attacker_damage,
            "defender_damage": defender_damage,
            "attacker_damage_is_magic": False,
            "defender_damage_is_magic": False,
        }
        return attack_info

    def get_defense_info(self, attacker_character: Character, defender_character: Character):
        # TODO: add terrain/support effects
        return {
            "attacker_defense": attacker_character.character_statistics.defense,
            "attacker_resistance": attacker_character.character_statistics.resistance,
            "defender_defense": defender_character.character_statistics.defense,
            "defender_resistance": defender_character.character_statistics.resistance,
        }

    def get_damage_info(self, attacker_character: Character, defender_character: Character):
        attack_info = self.get_attack_info(attacker_character, defender_character)
        defense_info = self.get_defense_info(attacker_character, defender_character)
        return {
            "attacker_damage": attack_info["attacker_damage"] - defense_info["defender_resistance"]
            if attack_info["attacker_damage_is_magic"]
            else attack_info["attacker_damage"] - defense_info["defender_defense"],
            "defender_damage": attack_info["defender_damage"] - defense_info["attacker_resistance"]
            if attack_info["defender_damage_is_magic"]
            else attack_info["defender_damage"] - defense_info["attacker_defense"],
        }

    def get_attack_speed_info(self, attacker_character: Character, defender_character: Character):
        attacker_speed = (
            attacker_character.character_statistics.speed
            + attacker_character.character_statistics.constitution
            - attacker_character.weapon_equip.weight
        )
        defender_speed = (
            defender_character.character_statistics.speed
            + defender_character.character_statistics.constitution
            - defender_character.weapon_equip.weight
        )
        attacker_double_hit = (attacker_speed - defender_speed) >= self.attack_speed_double_hit_threshold
        defender_double_hit = (defender_speed - attacker_speed) >= self.attack_speed_double_hit_threshold
        return {
            "attacker_speed": attacker_speed,
            "defender_speed": defender_speed,
            "attacker_double_hit": attacker_double_hit,
            "defender_double_hit": defender_double_hit,
        }

    def _get_hit_rate_info(
        self,
        attacker_character: Character,
        defender_character: Character,
        attacker_hit_bonus: int = 0,
        defender_hit_bonus: int = 0,
    ):
        # TODO: hit rate for magic related spells
        weapon_triangle_bonus = self.get_weapon_triangle_bonus(attacker_character, defender_character)
        attacker_weapon_hit = attacker_character.weapon_equip.hit
        defender_weapon_hit = defender_character.weapon_equip.hit
        attacker_skill = attacker_character.character_statistics.skill
        defender_skill = defender_character.character_statistics.skill
        attacker_luck = attacker_character.character_statistics.luck
        defender_luck = defender_character.character_statistics.luck
        attacker_triangle_hit_value = float(weapon_triangle_bonus.get("triangle_hit_value", 0))
        defender_triangle_hit_value = float(weapon_triangle_bonus.get("triangle_hit_value", 0)) * -1
        attacker_hit_value = (
            attacker_weapon_hit
            + (2 * attacker_skill)
            + (attacker_luck / 2)
            + attacker_triangle_hit_value
            + attacker_hit_bonus
        )
        defender_hit_value = (
            defender_weapon_hit
            + (2 * defender_skill)
            + (defender_luck / 2)
            + defender_triangle_hit_value
            + defender_hit_bonus
        )
        return {"attacker_hit_value": attacker_hit_value, "defender_hit_value": defender_hit_value}

    def _get_avoid_rate_info(
        self,
        attacker_character: Character,
        defender_character: Character,
        attacker_avoid_bonus: int = 0,
        defender_avoid_bonus: int = 0,
        attacker_terrain_bonus: int = 0,
        defender_terrain_bonus: int = 0,
    ):
        attack_speed_info = self.get_attack_speed_info(attacker_character, defender_character)
        attacker_attack_speed = attack_speed_info["attacker_speed"]
        defender_attack_speed = attack_speed_info["defender_speed"]
        attacker_luck = attacker_character.character_statistics.luck
        defender_luck = defender_character.character_statistics.luck
        attacker_avoid_rate = 2 * attacker_attack_speed + attacker_luck + attacker_avoid_bonus + attacker_terrain_bonus
        defender_avoid_rate = 2 * defender_attack_speed + defender_luck + defender_avoid_bonus + defender_terrain_bonus
        return {"attacker_avoid_rate": attacker_avoid_rate, "defender_avoid_rate": defender_avoid_rate}

    def get_hit_rate_info(
        self,
        attacker_character: Character,
        defender_character: Character,
        attacker_hit_bonus: int = 0,
        defender_hit_bonus: int = 0,
        attacker_avoid_bonus: int = 0,
        defender_avoid_bonus: int = 0,
        attacker_terrain_bonus: int = 0,
        defender_terrain_bonus: int = 0,
    ):
        hit_info = self._get_hit_rate_info(
            attacker_character, defender_character, attacker_hit_bonus, defender_hit_bonus
        )
        avoid_info = self._get_avoid_rate_info(
            attacker_character,
            defender_character,
            attacker_avoid_bonus,
            defender_avoid_bonus,
            attacker_terrain_bonus,
            defender_terrain_bonus,
        )
        # NOTE: use "true hit" RNG, that is roll 2 numbers and take the average
        attacker_hit_value = hit_info["attacker_hit_value"] - avoid_info["defender_avoid_rate"]
        defender_hit_value = hit_info["defender_hit_value"] - avoid_info["attacker_avoid_rate"]

        attacker_hit_percentage = DistributionUtil.get_true_hit_proba(attacker_hit_value)
        defender_hit_percentage = DistributionUtil.get_true_hit_proba(defender_hit_value)

        return {
            "attacker_hit_value": attacker_hit_value,
            "defender_hit_value": defender_hit_value,
            "attacker_hit_percentage": attacker_hit_percentage,
            "defender_hit_percentage": defender_hit_percentage,
        }

    def _get_crit_rate_info(
        self,
        attacker_character: Character,
        defender_character: Character,
        attacker_crit_bonus: int = 0,
        defender_crit_avoid_bonus: int = 0,
    ):
        attacker_skill = attacker_character.character_statistics.skill
        attacker_weapon_crit = attacker_character.weapon_equip.crit
        defender_luck = defender_character.character_statistics.luck

        attacker_crit_stat = max(attacker_skill - 10, 0) + attacker_weapon_crit + attacker_crit_bonus
        defender_crit_avoid = defender_luck + defender_crit_avoid_bonus
        attacker_crit = attacker_crit_stat - defender_crit_avoid
        return attacker_crit

    def get_crit_rate_info(
        self,
        attacker_character: Character,
        defender_character: Character,
        attacker_crit_bonus: int = 0,
        defender_crit_bonus: int = 0,
        attacker_crit_avoid_bonus: int = 0,
        defender_crit_avoid_bonus: int = 0,
    ):
        return {
            "attacker_crit": self._get_crit_rate_info(
                attacker_character, defender_character, attacker_crit_bonus, defender_crit_avoid_bonus
            ),
            "defender_crit": self._get_crit_rate_info(
                defender_character, attacker_character, defender_crit_bonus, attacker_crit_avoid_bonus
            ),
        }

    def display_combat_info(self, attacker_character: Character, defender_character: Character):
        info = {}

        attack_info = self.get_attack_info(attacker_character, defender_character)
        defense_info = self.get_defense_info(attacker_character, defender_character)
        damage_info = self.get_damage_info(attacker_character, defender_character)
        attack_speed_info = self.get_attack_speed_info(attacker_character, defender_character)
        hit_rate_info = self.get_hit_rate_info(attacker_character, defender_character)
        crit_info = self.get_crit_rate_info(attacker_character, defender_character)

        info.update(attack_info)
        info.update(defense_info)
        info.update(damage_info)
        info.update(attack_speed_info)
        info.update(hit_rate_info)
        info.update(crit_info)

        return info
