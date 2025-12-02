"""
command.py — Analyse et exécution des commandes du joueur.

Ce module contient la classe Command, responsable :
- d'interpréter le texte tapé par le joueur,
- d'identifier le verbe et l’argument,
- d’appeler la fonction correspondante du module actions.py.

La classe agit comme un routeur central des interactions,
permettant de séparer la logique de gameplay (actions.py)
de la gestion du texte entré par l’utilisateur.
"""

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
    check, 
    cheat,
    analyze
)


class Command:
    """
    Représente une commande textuelle entrée par le joueur.

    Exemple : "prendre clef", "aller nord", "attaquer garde"

    Attributs :
        raw (str) : texte original.
        verb (str) : premier mot de la commande (action à exécuter).
        arg (str|None) : argument éventuel (objet, direction, nom d’ennemi…).

    La méthode principale est execute(), qui appelle l’action associée.
    """

    def __init__(self, raw: str):
        """Initialise la commande à partir du texte brut."""
        self.raw = raw.strip()
        self.verb = ""
        self.arg = None

    def parse(self):
        """
        Analyse la commande :
        - Sépare le verbe (ex : "prendre")
        - De l'argument (ex : "épée")

        Exemple :
            "prendre épée" → verb="prendre", arg="épée"
        """
        parts = self.raw.split(maxsplit=1)
        self.verb = parts[0].lower() if parts else ""
        self.arg = parts[1] if len(parts) > 1 else None

    def execute(self, game):
        """
        Exécute la commande en fonction du verbe identifié.

        Étapes :
            1) parse() pour extraire verbe + argument
            2) appli applique les règles de combat (limitation des actions)
            3) routage vers la bonne fonction dans actions.py

        Retour :
            str — le texte à afficher au joueur.
        """
        self.parse()
        v = self.verb
        a = self.arg

        if not v:
            return ""

        # -----------------------------
        #  Blocage des actions en combat
        # -----------------------------
        if game.in_combat:
            allowed = {
                "attaquer", "attack", "a",
                "utiliser", "use", "u",
                "statut", "status", "s",
                "ia", "inventory", "inventaire",
                "check", "examiner" "analyze", "b",
            }
            if v not in allowed:
                return (
                    "❌ Vous êtes en combat : utilisez 'attaquer', 'utiliser', "
                    "'statut', 'ia', 'inventaire' ou 'examiner'."
                )

        # -----------------------------
        #  Déplacements
        # -----------------------------
        if v in ("aller", "go", "g"):
            return go(game, a)
        if v in ("retour", "back"):
            return back(game)

        # -----------------------------
        #  Observation
        # -----------------------------
        if v in ("observer", "look", "o"):
            return look(game)

        # -----------------------------
        #  Gestion des objets
        # -----------------------------
        if v in ("prendre", "take", "p"):
            return take(game, a)
        if v in ("jeter", "drop", "j"):
            return drop(game, a)
        if v in ("inventaire", "inventory", "i"):
            return inventory(game)
        if v in ("examiner", "check", "e"):
            return check(game, a)

        # -----------------------------
        #  PNJ
        # -----------------------------
        if v in ("parler", "talk", "t"):
            return talk(game, a)

        # -----------------------------
        #  Combat
        # -----------------------------
        if v in ("attaquer", "attack", "a"):
            return attack(game, a)
        if v in ("tricher", "cheat", "b"):
            return cheat(game, a)

        # -----------------------------
        #  Utilisation d'objet
        # -----------------------------
        if v in ("utiliser", "use", "u"):
            return use(game, a)

        # -----------------------------
        #  Informations / Statistiques
        # -----------------------------
        if v in ("statut", "status", "s"):
            return status(game)
        if v in ("historique", "history", "h"):
            return history(game)
        if v in ("ia", "ai"):
            return ai_status(game)
        if v in ("analyser", "analyze", "x"):
            return analyze(game, a)

        # -----------------------------
        #  Quitter le jeu
        # -----------------------------
        if v in ("quitter", "quit", "exit", "q"):
            return quit_game(game)

        return f"Commande inconnue : {v}"
