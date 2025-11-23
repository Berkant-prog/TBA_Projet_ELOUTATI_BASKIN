# character.py
"""
Classe Character : personnage non joueur (PNJ).

Attributs
---------
name : str
    Nom du personnage.
description : str
    Description courte.
current_room : Room
    Lieu actuel du PNJ.
msgs : list[str]
    Messages cycliques que le PNJ peut dire.

Méthodes
--------
__str__() -> str
    Représentation textuelle du PNJ.
get_msg() -> str
    Retourne un message (tourne en boucle dans msgs).
"""

class Character:
    """Personnage non joueur du jeu."""

    def __init__(self, name, description, current_room, msgs):
        self.name = name
        self.description = description
        self.current_room = current_room
        self.msgs = list(msgs) if msgs else []
        self._msg_index = 0

    def __str__(self):
        return f"{self.name} : {self.description}"

    def get_msg(self):
        """Retourne un des messages du PNJ, en boucle."""
        if not self.msgs:
            return f"{self.name} reste silencieux..."

        msg = self.msgs[self._msg_index]
        self._msg_index = (self._msg_index + 1) % len(self.msgs)
        return msg
