"""
enemy.py — Définit la classe Enemy, représentant un ennemi combattable.

Un ennemi possède :
- des statistiques de combat (HP, ATK, DEF),
- un statut (boss ou non),
- un éventuel loot (objet(s) laissés après sa mort).

Cette classe encapsule toute la logique liée au combat côté ennemi :
réception de dégâts, état vivant/mort, description textuelle.
"""

from item import Item


class Enemy:
    """
    Représente un ennemi que le joueur peut affronter.

    Paramètres :
        name (str) : nom de l’ennemi.
        hp (int) : points de vie.
        atk (int) : puissance d’attaque.
        defense (int) : défense réduisant les dégâts subis.
        is_boss (bool) : True si l’ennemi est un boss.
        loot (Item | list[Item]) : objets laissés à la mort.
        boss : compatibilité ancienne (boss=True ⇒ is_boss True).

    L’ennemi gère lui-même la prise de dégâts via take_damage().
    """

    def __init__(
        self,
        name: str,
        hp: int,
        atk: int,
        defense: int,
        is_boss: bool = False,
        loot=None,
        boss=None,  # compatibilité avec anciens scripts
    ):
        # Compatibilité : si le constructeur reçoit boss=, on l'utilise
        if boss is not None:
            is_boss = boss

        self.name = name
        self.hp = hp
        self.atk = atk
        self.defense = defense
        self.is_boss = is_boss

        # Si loot est un seul item, on le met dans une liste
        # Si None → liste vide
        self.loot = loot or []  # list[Item]

    def is_alive(self) -> bool:
        """Retourne True si l’ennemi est encore en vie (HP > 0)."""
        return self.hp > 0

    def take_damage(self, amount: int) -> int:
        """
        Applique des dégâts à l’ennemi et retourne les dégâts réellement infligés.

        amount (int) : dégâts de base avant réduction.

        Calcul :
            - Le dégâts ne peuvent pas être négatifs
            - La défense réduit les dégâts
            - Minimum 1 dégâts si amount > 0
        """
        amount = max(0, amount)

        if amount == 0:
            dmg = 0
        else:
            dmg = max(1, amount - self.defense)

        # Mise à jour des points de vie
        self.hp = max(0, self.hp - dmg)

        return dmg

    def __str__(self):
        """Représentation textuelle de l’ennemi (utile pour debug)."""
        return f"{self.name} (HP {self.hp}, ATK {self.atk}, DEF {self.defense})"
