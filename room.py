# room.py
"""
Classe Room : représente un lieu du jeu.

Attributs
---------
name : str
    Nom du lieu.
description : str
    Description textuelle du lieu.
exits : dict[str, Room]
    Dictionnaire des sorties, indexé par une direction (N, S, E, W, U, D).
inventory : list[Item]
    Liste des objets présents dans la pièce.
characters : list[Character]
    Liste des personnages non-joueurs présents.
enemies : list[Enemy]
    Liste des ennemis présents.

Méthodes
--------
get_exit(direction: str) -> Room | None
    Retourne la salle dans la direction donnée, ou None.
get_exit_string() -> str
    Retourne une description textuelle des sorties.
get_inventory() -> str
    Retourne une description textuelle des objets présents.
get_long_description() -> str
    Description complète du lieu (texte, sorties, PNJ, ennemis, commandes).
"""

class Room:
    """Lieu du jeu (une pièce, une zone, etc.)."""

    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.exits = {}          # dict[direction -> Room]
        self.inventory = []      # list[Item]
        self.characters = []     # list[Character]
        self.enemies = []        # list[Enemy]

    # --- Déplacements ---

    def get_exit(self, direction):
        """Retourne la salle associée à la direction donnée, ou None."""
        direction = direction.upper()
        return self.exits.get(direction, None)

    def get_exit_string(self):
        """Retourne une chaîne décrivant les sorties disponibles."""
        if not self.exits:
            return "Sorties: aucune"
        exit_string = "Sorties: "
        for direction, room in self.exits.items():
            if room is not None:
                exit_string += direction + ", "
        exit_string = exit_string.strip(", ")
        return exit_string

    # --- Inventaire de la pièce ---

    def get_inventory(self):
        """Retourne une chaîne décrivant les objets présents dans la pièce."""
        if not self.inventory:
            return "Il n'y a rien ici."
        lines = ["La pièce contient :"]
        for item in self.inventory:
            lines.append(f"- {item}")
        return "\n".join(lines)

    # --- Description complète ---

    def get_long_description(self):
        """Retourne une description longue : lieu, sorties, PNJ, ennemis, commandes."""
        lines = [f"\nVous êtes {self.description}", self.get_exit_string()]

        # PNJ
        if self.characters:
            pnj_names = ", ".join(c.name for c in self.characters)
            lines.append(f"Personnages présents : {pnj_names}")

        # Ennemis
        if self.enemies:
            enemy_names = ", ".join(e.name for e in self.enemies if e.is_alive())
            if enemy_names:
                lines.append(f"Ennemis détectés : {enemy_names}")

        # Objets
        lines.append(self.get_inventory())

        # Rappel des commandes
        lines.append(
            "\nCommandes : "
            "go <dir> | back | look | take <item> | drop <item> | check | "
            "talk <pnj> | attack <ennemi> | help | quit"
        )

        return "\n".join(lines)
