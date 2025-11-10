# character.py
# Classe de base pour tous les PNJ.

class Character:
    """Classe représentant un personnage non-joueur."""

    def __init__(self, name, dialogues, alignment="neutre"):
        """Initialise le PNJ avec son nom, ses dialogues et son alignement."""
        pass

    def talk(self, player):
        """Lance un dialogue avec le joueur."""
        pass

    def interact(self, player):
        """Définit un comportement spécifique (donner un objet, etc.)."""
        pass

    def give_item(self, player, item):
        """Offre un objet au joueur."""
        pass

