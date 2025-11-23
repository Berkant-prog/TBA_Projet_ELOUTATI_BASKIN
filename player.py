# player.py
"""
Classe Player : le joueur.

Attributs
---------
name : str
    Nom du joueur.
current_room : Room
    Lieu courant.
history : list[Room]
    Lieux précédemment visités (pile pour "back").
inventory : list[Item]
    Inventaire du joueur.
max_weight : int | float
    Poids maximal transportable.
hp : int
    Points de vie.
atk : int
    Attaque.
defense : int
    Défense.
has_crystal : bool
    Indique si le joueur possède le cristal de propulsion.

Méthodes
--------
move_to(room: Room) -> None
    Déplace le joueur vers un nouveau lieu et met à jour l'historique.
go_back() -> Room | None
    Revient au lieu précédent si possible.
get_history() -> str
    Affiche l'historique des lieux visités.
get_inventory() -> str
    Affiche l'inventaire.
carrying_weight() -> float
    Poids total porté.
can_take(item: Item) -> bool
    True si le joueur peut prendre l'objet.
"""

class Player:
    """Représente le joueur et son état."""

    def __init__(self, name, starting_room, max_weight=10):
        self.name = name
        self.current_room = starting_room
        self.history = []        # pile de Room
        self.inventory = []      # list[Item]
        self.max_weight = max_weight

        # Stats de base (combat)
        self.hp = 20
        self.atk = 6
        self.defense = 2

        # Quête principale
        self.has_crystal = False

    # --- Déplacement et historique ---

    def move_to(self, room):
        """Déplace le joueur et mémorise l'ancienne pièce dans l'historique."""
        if self.current_room is not None:
            self.history.append(self.current_room)
        self.current_room = room

    def go_back(self):
        """Revient à la pièce précédente si possible, sinon None."""
        if not self.history:
            return None
        previous = self.history.pop()
        self.current_room = previous
        return previous

    def get_history(self):
        """Retourne une description de l'historique des lieux visités."""
        if not self.history:
            return ""
        lines = ["Vous avez déjà visité les pièces suivantes :"]
        # On affiche les descriptions des pièces (sans doublon éventuel)
        seen = set()
        for room in self.history:
            if room.description not in seen:
                seen.add(room.description)
                lines.append(f"- {room.description}")
        return "\n".join(lines)

    # --- Inventaire ---

    def carrying_weight(self):
        """Retourne le poids total des objets portés."""
        return sum(item.weight for item in self.inventory)

    def can_take(self, item):
        """True si le joueur peut prendre l'objet (poids max non dépassé)."""
        return self.carrying_weight() + item.weight <= self.max_weight

    def get_inventory(self):
        """Retourne une description de l'inventaire du joueur."""
        if not self.inventory:
            return "Votre inventaire est vide."
        lines = ["Vous disposez des items suivants :"]
        for item in self.inventory:
            lines.append(f"- {item}")
        lines.append(f"Poids total : {self.carrying_weight()} / {self.max_weight} kg")
        return "\n".join(lines)
