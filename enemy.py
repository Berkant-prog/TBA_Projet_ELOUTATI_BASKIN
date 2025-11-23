# enemy.py
"""
Classe Enemy : représentant un ennemi simple.

Attributs
---------
name : str
    Nom de l'ennemi.
description : str
    Description courte.
current_room : Room
    Lieu actuel de l'ennemi.
hp : int
    Points de vie.
atk : int
    Points d'attaque (dégâts bruts).
loot : Item | None
    Objet laissé tomber à sa mort (facultatif).

Méthodes
--------
__str__() -> str
    Représentation textuelle.
is_alive() -> bool
    True si l'ennemi est encore en vie (> 0 PV).
"""

class Enemy:
    """Ennemi basique du jeu."""

    def __init__(self, name, description, current_room, hp, atk, loot=None):
        self.name = name
        self.description = description
        self.current_room = current_room
        self.hp = hp
        self.atk = atk
        self.loot = loot

    def __str__(self):
        return f"{self.name} : {self.description} (PV: {self.hp}, ATK: {self.atk})"

    def is_alive(self):
        return self.hp > 0
