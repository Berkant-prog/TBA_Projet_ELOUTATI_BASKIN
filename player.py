# player.py
# Classe représentant le joueur principal (héros du jeu)

class Player:
    """Représente le joueur : ses statistiques, son inventaire et sa position."""

    def __init__(self, name="Drake", starting_room=None):
        self.log = []  # historique des actions du joueur
        # --- Statistiques principales ---
        self.name = name
        self.hp = 100
        self.max_hp = 100
        self.atk = 10
        self.defense = 5
        self.energie = 100
        self.moral = 50
        self.reputation = 50

        # --- État / contexte ---
        self.inventory = []          # liste d'objets (Item)
        self.current_room = None     # référence vers l'objet Room actuel
        self.current_room = starting_room


    # -------------------------------
    # Gestion de l’inventaire
    # -------------------------------
    def add_item(self, item):
        """Ajoute un objet à l’inventaire."""
        self.inventory.append(item)
        return f"{item.name} ajouté à l’inventaire."

    def remove_item(self, item_name):
        """Retire un objet de l’inventaire par son nom."""
        for i, it in enumerate(self.inventory):
            if it.name.lower() == item_name.lower():
                return self.inventory.pop(i)
        return None

    def use_item(self, item_name):
        """Utilise un objet de l’inventaire."""
        item = self.remove_item(item_name)
        if not item:
            return "Objet introuvable dans votre inventaire."
        return item.use(self)

    def get_inventory(self):
        """Retourne la liste formatée des objets."""
        if not self.inventory:
            return "Inventaire vide."
        text = "Inventaire :\n"
        for it in self.inventory:
            text += f"- {it.name} ({it.effect_type}+{it.value})\n"
        return text.strip()

    # -------------------------------
    # Statut / affichage
    # -------------------------------
    def get_status(self):
        """Retourne un résumé complet des stats."""
        return (
            f"PV: {self.hp}/{self.max_hp} | ATK: {self.atk} | DEF: {self.defense}\n"
            f"Énergie: {self.energie} | Moral: {self.moral} | Réputation: {self.reputation}"
        )

    # -------------------------------
    # Gestion combat
    # -------------------------------
    def is_alive(self):
        """Retourne True si le joueur est encore en vie."""
        return self.hp > 0

    def take_damage(self, amount):
        """Fait subir des dégâts au joueur."""
        dmg = max(0, amount - self.defense)
        self.hp = max(0, self.hp - dmg)
        return dmg
    
    

    # -------------------------------
    # Historique d’actions
    # -------------------------------
    def log_event(self, text):
        """Ajoute un événement à l’historique du joueur."""
        if not hasattr(self, "log"):
            self.log = []
        if text:
            self.log.append(text)

    def get_history(self):
        """Retourne les dix dernières actions du joueur."""
        if not hasattr(self, "log") or not self.log:
            return "Aucun événement enregistré."
        return "Historique des actions :\n" + "\n".join(self.log[-10:])

