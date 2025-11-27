# enemy.py
"""Enemy class: basic combat stats and loot."""

from item import Item

class Enemy:
    def __init__(
        self,
        name: str,
        hp: int,
        atk: int,
        defense: int,
        is_boss: bool = False,
        loot=None,
        boss=None,         # backward compat if 'boss=' was used
    ):
        if boss is not None:
            is_boss = boss

        self.name = name
        self.hp = hp
        self.atk = atk
        self.defense = defense
        self.is_boss = is_boss
        self.loot = loot or []  # list[Item]

    def is_alive(self) -> bool:
        return self.hp > 0

    def take_damage(self, amount: int) -> int:
        """Return actual damage inflicted (after defense)."""
        amount = max(0, amount)
        if amount == 0:
            dmg = 0
        else:
            dmg = max(1, amount - self.defense)
        self.hp = max(0, self.hp - dmg)
        return dmg

    def __str__(self):
        return f"{self.name} (HP {self.hp}, ATK {self.atk}, DEF {self.defense})"
