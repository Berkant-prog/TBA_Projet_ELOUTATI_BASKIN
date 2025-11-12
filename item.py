# item.py
# Classe de base pour les objets manipulables dans le jeu

class Item:
    """Objet du jeu : améliore les stats, débloque des zones, etc."""

    def __init__(self, name, description, effect_type, value=0, usable=True):
        """
        Initialise un objet.
        :param name: nom de l’objet
        :param description: description textuelle
        :param effect_type: type d’effet ('atk', 'def', 'hp', 'energie', etc.)
        :param value: valeur numérique de l’effet
        :param usable: si l’objet peut être utilisé par le joueur
        """
        self.name = name
        self.description = description
        self.effect_type = effect_type
        self.value = value
        self.usable = usable

    def use(self, player):
        """
        Applique l’effet de l’objet sur le joueur.
        """
        if not self.usable:
            return f"L’objet {self.name} ne peut pas être utilisé."

        if self.effect_type == "atk":
            player.atk += self.value
            return f"{player.name} équipe {self.name}, attaque +{self.value}."
        elif self.effect_type == "def":
            player.defense += self.value
            return f"{player.name} équipe {self.name}, défense +{self.value}."
        elif self.effect_type == "hp":
            player.hp = min(player.max_hp, player.hp + self.value)
            return f"{player.name} soigne {self.value} PV."
        elif self.effect_type == "energie":
            player.energie = min(100, player.energie + self.value)
            return f"{player.name} regagne {self.value} points d’énergie."
        elif self.effect_type == "moral":
            player.moral = min(100, player.moral + self.value)
            return f"{player.name} retrouve du moral (+{self.value})."
        elif self.effect_type == "reputation":
            player.reputation = min(100, player.reputation + self.value)
            return f"La réputation de {player.name} augmente (+{self.value})."
        else:
            return f"L’objet {self.name} n’a pas d’effet particulier."

    def __repr__(self):
        """Représentation pour debug."""
        return f"<Item {self.name}: {self.effect_type}+{self.value}>"
