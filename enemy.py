# enemy.py
# Gestion des ennemis et du système de combat

class Enemy:
    """Classe représentant un ennemi dans le jeu."""

    def __init__(self, name, hp, atk, defense, is_boss=False, loot=None):
        self.name = name
        self.hp = hp
        self.max_hp = hp
        self.atk = atk
        self.defense = defense
        self.is_boss = is_boss
        self.loot = loot  # nom de l’objet lâché ou None

    def attack(self, player):
        """Inflige des dégâts au joueur et renvoie le nombre de dégâts infligés."""
        dmg = max(0, self.atk - player.defense)
        player.hp = max(0, player.hp - dmg)
        return dmg

    def take_damage(self, value):
        """Subit des dégâts (après défense) et renvoie le nombre de dégâts subis."""
        dmg = max(0, value - self.defense)
        self.hp = max(0, self.hp - dmg)
        return dmg

    def is_alive(self):
        """Retourne True si l'ennemi est encore en vie."""
        return self.hp > 0

    def drop_loot(self):
        """Renvoie le butin lâché par l’ennemi s’il en possède un."""
        return self.loot

    def __repr__(self):
        return f"<Enemy {self.name}: HP={self.hp}/{self.max_hp}, ATK={self.atk}, DEF={self.defense}>"
