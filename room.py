# room.py
# Représente une planète / une zone.

class Room:
    """Lieu/planète avec connexions, PNJ, ennemis, objets."""

    def __init__(self, name, description, connected_rooms=None, items=None, pnj=None, enemies=None):
        self.name = name
        self.description = description
        self.connected_rooms = connected_rooms or {}  # {"est": "Velyra IX"}
        self.items = items or []                      # liste d'instances Item
        self.pnj = pnj or []                          # instances Character
        self.enemies = enemies or []                  # instances Enemy
        self.visited = False

    def describe(self):
        """Retour d’une description formatée pour l’affichage."""
        self.visited = True
        lines = [f"\n== {self.name} ==", self.description]
        if self.pnj:
            lines.append("Personnages présents : " + ", ".join(p.name for p in self.pnj))
        alive_names = [e.name for e in self.enemies if e.is_alive()]
        if alive_names:
            lines.append("Ennemis détectés : " + ", ".join(alive_names))
        if self.items:
            lines.append("Objets visibles : " + ", ".join(i.name for i in self.items))
        if self.connected_rooms:
            dirs = ", ".join(f"{d}→{n}" for d, n in self.connected_rooms.items())
            lines.append(f"Sorties : {dirs}")
        return "\n".join(lines)

    def get_connections(self):
        return dict(self.connected_rooms)

    def add_item(self, item):
        self.items.append(item)

    def remove_item(self, item_name):
        """Retire un objet par son nom et le renvoie (ou None)."""
        for i, it in enumerate(self.items):
            if it.name.lower() == item_name.lower():
                return self.items.pop(i)
        return None

    def has_enemy(self):
        """True s'il reste au moins un ennemi vivant."""
        return any(e.is_alive() for e in self.enemies)

    def get_enemy(self, name=None):
        """Retourne l’ennemi ciblé (par nom) ou le premier encore vivant."""
        alive = [e for e in self.enemies if e.is_alive()]
        if not alive:
            return None
        if name is None:
            return alive[0]
        for e in alive:
            if e.name.lower() == name.lower():
                return e
        return None
