"""
character.py — Gestion des personnages non jouables (NPC).

Ce module définit la classe Character, utilisée pour représenter
les PNJ présents dans les différentes pièces du jeu. Un PNJ peut :

- Afficher une description
- Avoir plusieurs lignes de dialogue
- Répondre avec un message cyclique
- Déclencher une fonction spéciale lorsqu’on lui parle (callback on_talk)

Il s’agit de la base des interactions narratives avec le joueur.
"""

class Character:
    """
    Représente un personnage non-joueur (PNJ).

    Attributs :
        name (str) : nom du personnage.
        description (str) : description affichée dans la pièce.
        messages (list[str]) : liste de messages que le PNJ peut dire.
                               Si plusieurs sont fournis, ils défilent à chaque interaction.
        _msg_index (int) : index interne pour alterner les messages.
        on_talk (callable) : fonction optionnelle appelée lorsqu'on parle au PNJ.
                             Signature attendue : on_talk(player, game, self)
    """

    def __init__(self, name: str, description: str, messages=None):
        """Initialise un PNJ avec son nom, sa description et ses éventuels messages."""
        self.name = name
        self.description = description
        self.messages = messages or []
        self._msg_index = 0

        # Callback facultatif permettant un comportement personnalisé
        self.on_talk = None

    def talk(self, player, game=None):
        """
        Renvoie la réplique actuelle du PNJ lorsqu'on lui parle.

        Fonctionnement :
        - Si un callback on_talk est défini → il est appelé.
        - Sinon, le PNJ dit le prochain message de sa liste.
        - Si aucun message n'est défini → réponse par défaut (“reste silencieux”).

        Paramètres :
            player : l'objet joueur interagissant avec le PNJ.
            game : l'objet Game (optionnel), si le PNJ doit interagir avec l’état du jeu.

        Retour :
            str — le message prononcé par le PNJ.
        """
        # Callback personnalisé
        if callable(self.on_talk):
            return self.on_talk(player, game, self)

        # Aucun message défini
        if not self.messages:
            return f"{self.name} reste silencieux."

        # Dialogue cyclique
        msg = self.messages[self._msg_index]
        self._msg_index = (self._msg_index + 1) % len(self.messages)
        return f"{self.name}: {msg}"

    def __str__(self):
        """Retourne la chaîne de présentation du PNJ (utile pour debug ou inventaire)."""
        return f"{self.name}: {self.description}"
