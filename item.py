# item.py
# Définit les objets utilisables dans le jeu.

class Item:
    """Classe représentant un objet du jeu."""

    def __init__(self, name, description, effect_type, value, usable=True):
        """Initialise un objet avec son nom et son effet."""
        pass

    def use(self, player):
        """Applique l’effet de l’objet au joueur."""
        pass

    def inspect(self):
        """Retourne une description détaillée de l’objet."""
        pass

