# room.py
"""Room class for the Vigilant TBA game."""

class Room:
    def __init__(self, name, description):
        self.name = name
        self.description = description

        # Exits = {"N": room, "E": room, ...}
        self.exits = {}

        # Content of the room
        self.items = []
        self.characters = []
        self.enemies = []

    # ============================================================
    # CONNECTIONS
    # ============================================================
    def connect(self, other_room, direction):
        """
        Connect two rooms bidirectionally.
        direction: 'N', 'E', 'S', 'O', 'H', 'B'
        """
        self.exits[direction.upper()] = other_room

        # Create reverse link
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
        direction = direction.upper()
        return self.exits.get(direction, None)

    # ============================================================
    # ITEMS
    # ============================================================
    def add_item(self, item):
        self.items.append(item)

    def remove_item(self, item):
        if item in self.items:
            self.items.remove(item)

    def find_item(self, name):
        name = name.lower()
        for it in self.items:
            if it.name.lower() == name:
                return it
        return None

    # ============================================================
    # CHARACTERS (NPC)
    # ============================================================
    def add_character(self, character):
        self.characters.append(character)

    def find_character(self, name):
        name = name.lower()
        for c in self.characters:
            if c.name.lower() == name:
                return c
        return None

    # ============================================================
    # ENEMIES
    # ============================================================
    def add_enemy(self, enemy):
        self.enemies.append(enemy)

    def find_enemy(self, name):
        name = name.lower()
        for e in self.enemies:
            if e.name.lower() == name and e.is_alive():
                return e
        return None

    # ============================================================
    # DESCRIPTION
    # ============================================================
    def get_exit_string(self):
        if not self.exits:
            return "Aucune sortie."

        # Conversion directions EN -> FR
        dir_fr = {
            "N": "N",
            "S": "S",
            "E": "E",
            "O": "O",   # ← important : W devient O pour Ouest
            "H": "H",   # Haut
            "B": "B",   # Bas
        }

        lines = ["Sorties :"]
        for direction, room in self.exits.items():
            d = dir_fr.get(direction, direction)
            lines.append(f"  {d} → {room.name}")

        return "\n".join(lines)




    def get_long_description(self):
        desc = f"== {self.name} ==\n{self.description}\n"
        
        if self.characters:
            desc += "Personnes présentes : " + ", ".join(c.name for c in self.characters) + "\n"

        if self.enemies:
            desc += "Ennemis : " + ", ".join(e.name for e in self.enemies if e.is_alive()) + "\n"

        if self.items:
            desc += "Objets : " + ", ".join(i.name for i in self.items) + "\n"

        desc += self.get_exit_string()
        return desc

