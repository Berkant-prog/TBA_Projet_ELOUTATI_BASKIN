from actions import (
    go,
    back,
    look,
    take,
    drop,
    inventory,
    talk,
    attack,
    use,
    status,
    history,
    ai_status,
    quit_game,
    check
)

class Command:
    """Analyse et exécute une commande textuelle."""

    def __init__(self, raw: str):
        self.raw = raw.strip()
        self.verb = ""
        self.arg = None

    def parse(self):
        parts = self.raw.split(maxsplit=1)
        self.verb = parts[0].lower() if parts else ""
        self.arg = parts[1] if len(parts) > 1 else None

    def execute(self, game):
        self.parse()
        v = self.verb
        a = self.arg

        if not v:
            return ""

        # Blocage en combat
        if game.in_combat:
            allowed = {"attaquer", "attack", "a", 
                       "utiliser", "use", "u",
                       "statut", "status", "s",
                       "ia", "inventory", "inventaire",
                       "check", "examiner"}
            if v not in allowed:
                return "❌ Vous êtes en combat : utilisez 'attaquer', 'utiliser', 'statut', 'ia', 'inventaire' ou 'examiner'."

        # Déplacements
        if v in ("aller", "go", "g"):
            return go(game, a)
        if v in ("retour", "back"):
            return back(game)

        # Observation
        if v in ("observer", "look", "o"):
            return look(game)

        # Objets
        if v in ("prendre", "take", "p"):
            return take(game, a)
        if v in ("jeter", "drop", "j"):
            return drop(game, a)
        if v in ("inventaire", "inventory", "i"):
            return inventory(game)
        if v in ("examiner", "check", "e"):
            return check(game, a)

        # PNJ
        if v in ("parler", "talk", "t"):
            return talk(game, a)

        # Combat
        if v in ("attaquer", "attack", "a"):
            return attack(game, a)

        # Utiliser un objet
        if v in ("utiliser", "use", "u"):
            return use(game, a)

        # Information
        if v in ("statut", "status", "s"):
            return status(game)
        if v in ("historique", "history", "h"):
            return history(game)
        if v in ("ia", "ai"):
            return ai_status(game)

        # Quitter
        if v in ("quitter", "quit", "exit", "q"):
            return quit_game(game)

        return f"Commande inconnue : {v}"
