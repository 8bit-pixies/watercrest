from watercrest.entity.weapon import WeaponTriangle
from watercrest.entity.weapon import WeaponCategory
from watercrest.entity.weapon import WeaponInfo
from watercrest.service.weapon_triangle_service import WeaponTriangleService


def test_all_losing_combinations():
    for attk, defd in [
        (WeaponCategory.AXE, WeaponCategory.SWORD),
        (WeaponCategory.SWORD, WeaponCategory.LANCE),
        (WeaponCategory.LANCE, WeaponCategory.AXE),
    ]:
        weapon_triangle = WeaponTriangleService()
        attk_info = WeaponInfo(weapon_category=attk)
        defd_info = WeaponInfo(weapon_category=defd)
        assert weapon_triangle.weapon_triangle_outcome(attk_info, defd_info) == WeaponTriangle.LOSING, (attk, defd)


def test_weapon_from_config():
    iron_sword = WeaponInfo.from_config("iron sword")
    wo_dao = WeaponInfo.from_config("wo dao")
    weapon_triangle = WeaponTriangleService()
    print(wo_dao, iron_sword)
    assert weapon_triangle.weapon_triangle_outcome(iron_sword, wo_dao) == WeaponTriangle.NEUTRAL
