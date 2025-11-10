# command.py
# Analyse et exécution des commandes saisies par le joueur.

class Command:
    """Classe pour interpréter les commandes du joueur."""

    def __init__(self, raw_input):
        """Stocke la commande brute saisie."""
        pass

    def parse(self):
        """Analyse le texte et sépare verbe / cible."""
        pass

    def execute(self, game):
        """Appelle la bonne fonction dans actions.py selon la commande."""
        pass

