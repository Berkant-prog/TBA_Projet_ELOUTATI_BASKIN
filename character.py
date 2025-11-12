# character.py
# Classe de base pour tous les PNJ (non hostiles ou neutres).

class Character:
    """Personnage non-joueur générique (allié, neutre…)."""

    def __init__(self, name, dialogues, alignment="neutral", gives_item=None):
        """
        Initialise le PNJ avec son nom, ses dialogues, son alignement
        et un éventuel objet à donner (gives_item).
        """
        self.name = name
        self.dialogues = dialogues or []
        self.alignment = alignment  # "ally", "neutral"
        self.gives_item = gives_item  # nom de l’objet à offrir (optionnel)

    def talk(self, player):
        """Retourne une réplique simple (rotation basique)."""
        if not self.dialogues:
            return f"{self.name} reste silencieux…"
        # Variation légère selon moral/réputation du joueur
        idx = 0
        if player and player.moral > 60 and len(self.dialogues) > 1:
            idx = 1
        return f"{self.name}: {self.dialogues[idx]}"

    def interact(self, player):
        """Interaction simple : peut offrir un objet si conditions implicites remplies."""
        if self.gives_item:
            return f"{self.name} semble disposé à vous aider. (Essayez: 'prendre {self.gives_item}')"
        return f"{self.name} n’a rien à offrir pour le moment."
