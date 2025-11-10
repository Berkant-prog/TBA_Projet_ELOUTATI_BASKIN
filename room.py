# room.py
# Représente les planètes / lieux du jeu.

class Room:
    """Classe représentant un lieu ou une planète."""

    def __init__(self, name, description, connected_rooms=None, items=None, pnj=None):
        """Initialise la salle avec ses éléments."""
        pass

    def describe(self):
        """Affiche la description du lieu."""
        pass

    def get_connections(self):
        """Retourne les directions possibles."""
        pass

    def add_item(self, item):
        """Ajoute un objet dans la salle."""
        pass

    def remove_item(self, item):
        """Retire un objet de la salle."""
        pass

    def has_enemy(self):
        """Vérifie s’il y a un ennemi dans la salle."""
        pass

    def get_enemy(self):
        """Retourne l’ennemi présent s’il existe."""
        pass

