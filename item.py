"""
item.py — Définition de la classe Item.

Un Item représente un objet manipulable dans le jeu :
- il peut être ramassé, jeté, examiné,
- parfois utilisé pour produire un effet (soin, défense, quête…),
- il possède un poids influençant la capacité de transport du joueur.

Ce module est volontairement minimaliste : il agit comme un conteneur de données
que les actions (dans actions.py) interprètent.
"""


class Item:
    """
    Représente un objet du jeu.

    Attributs :
        name (str) :
            Nom de l'objet tel qu'il apparaît dans l'inventaire et dans les rooms.

        description (str) :
            Texte descriptif présenté lors de l'examen.

        effect_type (str) :
            Type d'effet appliqué lors de l'utilisation.
            Valeurs possibles (convention de jeu) :
                - "heal"  : rend des PV
                - "def"   : augmente la défense
                - "atk"   : augmente l'attaque
                - "quest" : objet clé de scénario, non utilisable
                - "misc"  : objet générique sans effet (par défaut)

        value (int) :
            Intensité de l'effet (ex : +25 PV, +2 DEF…).

        usable (bool) :
            Indique si l'objet peut être utilisé avec la commande "utiliser".

        weight (int) :
            Poids en kilogrammes, pour gérer la capacité de transport du joueur.

    Aucun comportement n'est codé ici : l'objet est une simple "fiche"
    que d'autres modules manipulent.
    """

    def __init__(
        self,
        name: str,
        description: str,
        effect_type: str = "misc",
        value: int = 0,
        usable: bool = False,
        weight: int = 1,
    ):
        """Initialise un objet avec ses propriétés principales."""
        self.name = name
        self.description = description
        self.effect_type = effect_type  # ex. "heal", "def", "quest"
        self.value = value
        self.usable = usable
        self.weight = weight

    def __str__(self):
        """Affichage lisible de l'objet (inventaire, sol, débug…)."""
        return f"{self.name}: {self.description} ({self.weight} kg)"
