# command.py
# Gère l'analyse et l'exécution des commandes saisies par le joueur.

class Command:
    """Analyse et exécute les commandes texte."""

    def __init__(self, raw):
        self.raw = raw.strip().lower()
        self.verb = None
        self.args = None

    def parse(self):
        """Analyse la commande utilisateur."""
        parts = self.raw.split(maxsplit=1)
        self.verb = parts[0] if parts else ""
        self.args = parts[1] if len(parts) > 1 else None

    def execute(self, game):
        """Exécute la commande analysée."""
        v = self.verb
        a = self.args

        if not v:
            return "(aucune commande saisie)"

        # === Déplacements ===
        if v in ["aller", "go"]:
            return game.do_aller(a)

        # === Observation ===
        if v in ["explorer", "observer", "regarder"]:
            return game.do_explorer()

        # === Dialogue ===
        if v == "parler":
            return game.do_parler(a)

        # === Objets ===
        if v == "prendre":
            return game.do_prendre(a)
        if v == "utiliser":
            return game.do_utiliser(a)
        if v == "inventaire":
            return game.do_inventaire()

        # === Combat ===
        if v in ["attaquer", "taper", "frapper"]:
            return game.do_attaquer(a)
        if v == "soigner":
            return game.do_soigner()
        if v == "fuir":
            return game.do_fuir()

        # === Info ===
        if v == "statut":
            return game.do_statut()
        if v == "historique":
            return game.do_historique()

        # === Debug (dev interne) ===
        if v == "debug":
            r = game.player.current_room
            enemies = [e.name for e in r.enemies if e.is_alive()]
            items = [i.name for i in r.items]
            pnj = [p.name for p in r.pnj]
            return (
                f"[DEBUG]\n"
                f"Salle: {r.name}\n"
                f"PNJ: {pnj}\n"
                f"Ennemis vivants: {enemies}\n"
                f"Objets: {items}\n"
                f"Stats: {game.player.get_status()}"
            )

        # === Quitter ===
        if v in ["quit", "exit", "quitter"]:
            return game.do_quitter()

        # === Commande inconnue ===
        return f"Commande inconnue: {v}"
