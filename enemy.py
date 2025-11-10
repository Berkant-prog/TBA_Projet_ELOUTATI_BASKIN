# enemy.py
# Définit les ennemis et le système de combat.

from character import Character

class Enemy(Character):
    """Classe représentant un ennemi, hérite de Character."""

    def __init__(self, name, hp, atk, defense, is_boss=False, loot=None):
        """Initialise les attributs d’un ennemi."""
        pass

    def attack(self, player):
        """Inflige des dégâts au joueur."""
        pass

    def take_damage(self, value):
        """Subit des dégâts."""
        pass

    def is_alive(self):
        """Retourne True si l’ennemi est encore en vie."""
        pass

    def drop_loot(self, player):
        """Donne un objet au joueur après la victoire."""
        pass

