"""
room.py — Définition des salles du jeu.

Une Room représente un lieu exploré par le joueur :
- elle possède un nom et une description narrative,
- des sorties (N/S/E/O/H/B) vers d’autres salles,
- des objets au sol,
- des personnages (PNJ),
- des ennemis potentiels.

Ce module sert de base à la structure de la carte du monde.
"""


class Room:
    """Représente une salle ou un lieu de l'univers du jeu."""

    def __init__(self, name, description):
        """
        Initialise une salle.

        Paramètres :
            name (str)         — nom du lieu
            description (str)  — texte narratif affiché au joueur
        """
        self.name = name
        self.description = description

        # Exits : dictionnaire direction → Room
        self.exits = {}

        # Contenu du lieu
        self.items = []
        self.characters = []
        self.enemies = []
        
        # Descriptions dynamique alternatives
        self.alt_description_robbery = ""
        self.alt_description_corruption = ""
        self.game = None  # Référence vers l'objet Game global

    # ============================================================
    # Connexions entre salles
    # ============================================================

    def connect(self, other_room, direction):
        """
        Connecte deux salles de manière bidirectionnelle.

        direction : 'N', 'E', 'S', 'O', 'H', 'B'

        Exemple : salleA.connect(salleB, "E")
        créera automatiquement la connexion salleB → salleA vers "O".
        """
        self.exits[direction.upper()] = other_room

        reverse = {
            "N": "S",
            "S": "N",
            "E": "O",
            "O": "E",
            "H": "B",
            "B": "H",
        }

        if direction.upper() in reverse:
            other_room.exits[reverse[direction.upper()]] = self

    def get_exit(self, direction):
        """Retourne la salle associée à une direction donnée, ou None."""
        direction = direction.upper()
        return self.exits.get(direction, None)

    # ============================================================
    # Gestion des objets
    # ============================================================

    def add_item(self, item):
        """Dépose un objet dans la salle."""
        self.items.append(item)

    def remove_item(self, item):
        """Retire un objet présent dans la salle."""
        if item in self.items:
            self.items.remove(item)

    def find_item(self, name):
        """Recherche un objet par nom, insensible à la casse."""
        name = name.lower()
        for it in self.items:
            if it.name.lower() == name:
                return it
        return None

    # ============================================================
    # PNJ (personnages non-joueurs)
    # ============================================================

    def add_character(self, character):
        """Ajoute un PNJ à la salle."""
        self.characters.append(character)

    def find_character(self, name):
        """Recherche un PNJ par son nom."""
        name = name.lower()
        for c in self.characters:
            if c.name.lower() == name:
                return c
        return None

    # ============================================================
    # Ennemis
    # ============================================================

    def add_enemy(self, enemy):
        """Ajoute un ennemi à la salle."""
        self.enemies.append(enemy)

    def find_enemy(self, name):
        """
        Recherche un ennemi vivant dans la salle.
        Retourne None si l’ennemi n'existe pas ou est déjà vaincu.
        """
        name = name.lower()
        for e in self.enemies:
            if e.name.lower() == name and e.is_alive():
                return e
        return None

    # ============================================================
    # Description longue
    # ============================================================

    def get_exit_string(self):
        """Retourne toutes les sorties avec le nom des salles reliées."""
        if not self.exits:
            return "Aucune sortie."

        dir_fr = {
            "N": "N",
            "S": "S",
            "E": "E",
            "O": "O",
            "H": "H",
            "B": "B",
        }

        lines = ["Sorties :"]
        for direction, room in self.exits.items():
            d = dir_fr.get(direction, direction)
            lines.append(f"  {d} → {room.name}")

        return "\n".join(lines)

    def get_long_description(self):
        """
        Retourne une description détaillée :
        - texte narratif,
        - PNJ,
        - ennemis vivants,
        - objets,
        - sorties.
        """
        desc = f"== {self.name} ==\n{self.description}\n"
        
        # Descriptions alternatives pour les entrepôts civils
        p = self.game.player
        if self.name == "Entrepôts civils":
            if getattr(p, "velyra_robbed_civilians", False):
                desc =  f"== {self.name} ==\n{self.alt_description_robbery}\n"
            elif getattr(p, "velyra_corrupted_general", False):
                desc =  f"== {self.name} ==\n{self.alt_description_corruption}\n"

        # Description alternative pour la prison centrale
        if self.name == "Prison centrale":      
            if getattr(p, "velyra_missiles_obtained", False):
                desc = f"== {self.name} ==\n{self.alt_description_after_missiles}\n"
            elif getattr(p, "velyra_prison_liberated", False):
                desc = f"== {self.name} ==\n{self.alt_description_after_raid}\n"
                
        # description alternative pour le district d'Or
        if self.name == "District d’Or":
            if getattr(self.game.player, "ap_choice_infiltrate", False):
                desc = f"== {self.name} ==\n{self.alt_description_infiltrate}\n"
            elif getattr(self.game.player, "ap_choice_reveal", False):
                desc = f"== {self.name} ==\n{self.alt_description_reveal}\n"

        # description alternative pour le Nœud
        if self.name == "Le Nœud":
            if getattr(self.game.player, "ap_break_illusions", False):
                desc = f"== {self.name} ==\n{self.alt_description_break}\n"
            elif getattr(self.game.player, "ap_keep_illusions", False):
                desc = f"== {self.name} ==\n{self.alt_description_keep}\n"


            
        if self.characters:
            desc += "Personnes présentes : " + ", ".join(c.name for c in self.characters) + "\n"

        if self.enemies:
            desc += "Ennemis : " + ", ".join(e.name for e in self.enemies if e.is_alive()) + "\n"

        if self.items:
            desc += "Objets : " + ", ".join(i.name for i in self.items) + "\n"

        desc += self.get_exit_string()
        return desc
