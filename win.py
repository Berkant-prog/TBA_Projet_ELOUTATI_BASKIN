# win.py
# Vérifie les fins du jeu selon l'état du Player.

from config import win_conditions as WC

class Win:
    """Règles de fin de partie (victoire/défaite/ambiguë)."""

    @staticmethod
    def check_victory(player):
        # Fin héroïque (renaissance)
        if player.moral >= WC["renaissance"]["moral_min"] and player.reputation >= WC["renaissance"]["reputation_min"]:
            return "renaissance"
        # Fin tyrannique (empire)
        if player.moral <= WC["empire"]["moral_max"] and player.reputation <= WC["empire"]["reputation_max"]:
            return "empire"
        return None

    @staticmethod
    def check_defeat(player):
        # Mort physique
        if player.hp <= 0:
            return "mort"
        # Panne/errance
        if player.energie <= WC["derive"]["energie_max"]:
            return "derive"
        return None

    @staticmethod
    def check_neutral_end(player):
        """Fin neutre si Kael est vaincu mais variables mixtes."""
        # Neutralité par défaut si pas d'autres fins déclenchées et boss final vaincu
        # (La logique exacte est gérée dans game.end_game() via drapeaux)
        return "ambigu"

    @staticmethod
    def show_ending(end_type):
        if end_type == "renaissance":
            return ("🌱 Renaissance d’ESIEE — Vous unissez les mondes et fondez la Nouvelle Terre.")
        if end_type == "empire":
            return ("⚔️ Empire d’Orion — La paix par la force. L’humanité survit, mais enchaînée.")
        if end_type == "mort":
            return ("💀 Vous succombez. Le Vigilant devient un mausolée dans le vide.")
        if end_type == "derive":
            return ("🌌 Écho du Néant — Le Vigilant dérive, dernier phare muet de l’humanité.")
        if end_type == "ambigu":
            return ("⚖️ Fin ambiguë — Victoire sans certitude. Votre nom devient un murmure d’étoiles.")
        return "Fin inconnue."
