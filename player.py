# player.py
# Gère le joueur, ses statistiques et son inventaire.

class Player:
    """Classe représentant le joueur."""

    def __init__(self, name, starting_room):
        """Initialise le joueur avec ses stats de base."""
        pass

    def move_to(self, room):
        """Change de salle / planète."""
        pass

    def take_damage(self, value):
        """Réduit les HP du joueur."""
        pass

    def heal(self, value):
        """Restaure des points de vie."""
        pass

    def add_item(self, item):
        """Ajoute un objet à l’inventaire."""
        pass

    def use_item(self, item):
        """Utilise un objet et applique ses effets."""
        pass

    def update_stats(self, atk=0, defense=0, energie=0, moral=0, reputation=0):
        """Met à jour les statistiques du joueur."""
        pass

    def show_inventory(self):
        """Affiche le contenu de l’inventaire."""
        pass

    def log_event(self, event):
        """Ajoute un événement à l’historique."""
        pass

    def get_status(self):
        """Retourne un résumé des stats actuelles."""
        pass

