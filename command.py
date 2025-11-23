# command.py
"""
Classe Command : analyse et exécute une commande texte.

Attributs
---------
raw : str
    Chaîne tapée par l'utilisateur.
verb : str
    Verbe de la commande (premier mot).
arg : str | None
    Argument éventuel (reste de la ligne).

Méthodes
--------
parse() -> None
    Analyse la chaîne brute pour séparer verbe et argument.
execute(game: Game) -> str
    Exécute la commande sur le jeu donné.
"""

from actions import (
    go,
    back,
    look,
    take,
    drop,
    check,
    talk,
    attack,
    show_help,
    quit_game,
)


class Command:
    """Analyse et exécute les commandes utilisateur."""

    def __init__(self, raw):
        self.raw = raw.strip()
        self.verb = ""
        self.arg = None

    def parse(self):
        """Analyse la commande en (verbe, argument)."""
        if not self.raw:
            self.verb = ""
            self.arg = None
            return
        parts = self.raw.split(maxsplit=1)
        self.verb = parts[0].lower()
        self.arg = parts[1] if len(parts) > 1 else None

    def execute(self, game):
        """Exécute la commande sur l'objet Game."""
        self.parse()

        # Commande vide : ne rien dire (contrairement à une commande inconnue).
        if not self.verb:
            return ""

        v = self.verb
        a = self.arg

        if v == "go":
            return go(game, a)
        if v == "back":
            return back(game)
        if v == "look":
            return look(game)
        if v == "take":
            return take(game, a)
        if v == "drop":
            return drop(game, a)
        if v == "check":
            return check(game)
        if v == "talk":
            return talk(game, a)
        if v == "attack":
            return attack(game, a)
        if v == "help":
            return show_help(game)
        if v == "quit":
            return quit_game(game)

        return f"Commande '{v}' non reconnue. Entrez 'help' pour voir l'aide."
