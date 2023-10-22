from enum import Enum


class CharacterClass(str, Enum):
    # Comment shows usable weapons, (+) indicates additional weapon upon promotion
    # TODO: add mages later
    ARCHER = "ARCHER"  # BOW
    BRIGAND = "BRIGAND"  # AXE
    CAVALIER = "CAVALIER"  # SWORD, LANCE - AXE(+)
    FIGHTER = "FIGHTER"  # AXE - BOW(+)
    KNIGHT = "KNIGHT"  # LANCE - AXE(+)
    MERCENARY = "MERCENARY"  # SWORD - AXE(+)
    MYRMIDON = "MYRMIDON"  # SWORD
    NOMAD = "NOMAD"  # BOW - SWORD(+)
    PEGASUS_KNIGHT = "PEGASUS_KNIGHT"  # LANCE - SWORD(+)
    WYVERN_RIDER = "WYVERN_RIDER"  # LANCE - SWORD(+)
