"""
player.py — Définition du joueur.

Cette classe regroupe :
- Les statistiques du capitaine (HP, ATK, DEF, moral…)
- L’inventaire et la gestion du poids transporté
- Le déplacement entre les salles et l’historique des lieux visités
- Les drapeaux de progression liés au scénario (Yara, Marchand, Cristal…)
- Les statistiques IA liées au mini-quiz influençant les combats

Le Player agit comme le conteneur central de l’état du jeu.
Toutes les actions (combat, déplacements, utilisation d’objets) s’appuient sur lui.
"""


class Player:
    """Représente le joueur et toutes ses données de progression."""

    def __init__(self, name: str, start_room):
        """
        Initialise un nouveau joueur.

        Paramètres :
            name (str)        — nom choisi par le joueur.
            start_room (Room) — première salle où commence l’aventure.
        """
        self.name = name

        # --- Statistiques de base ---
        self.hp = 100
        self.max_hp = 100
        self.atk = 8
        self.defense = 3
        self.moral = 0
        self.resources = 0

        # --- Inventaire ---
        self.inventory = []
        self.max_weight = 20
        self.current_weight = 0

        # --- Position & historique ---
        self.current_room = start_room
        self._room_history = []   # pile des salles traversées ("retour")
        self._event_log = []      # journal textuel des actions importantes

        # --- Drapeaux de progression / scénario ---
        self.has_translator = False
        self.has_crystal = False

        self.merchant_deal_done = False
        self.merchant_sacrifice = False
        self.merchant_refused = False

        self.met_yara = False
        self.met_ralen = False
        self.vorn_defeated = False

        # --- Statistiques IA ---
        self.ia_correct = 0
        self.ia_wrong = 0
        self.ia_questions_answered = 0

    # ============================================================
    # Déplacements
    # ============================================================

    def move_to(self, new_room):
        """
        Déplace le joueur vers une nouvelle salle.

        Enregistre aussi la salle précédente
        dans l'historique pour permettre 'retour'.
        """
        if self.current_room is not None:
            self.log(f"Vous êtes allé de {self.current_room.name} à {new_room.name}.")
            self._room_history.append(self.current_room)
        self.current_room = new_room

    def back(self):
        """
        Revient à la salle précédente si possible.

        Retourne :
            True  — si le retour est possible,
            False — sinon.
        """
        if not self._room_history:
            return False
        self.current_room = self._room_history[-1]
        self.log(f"Vous êtes retourné en arrière à {self.current_room.name}.")
        return True

    # ============================================================
    # Inventaire
    # ============================================================

    def add_item(self, item):
        """Ajoute un objet à l’inventaire et met à jour le poids total."""
        self.current_weight += item.weight
        self.inventory.append(item)

    def remove_item(self, item):
        """Retire un objet de l’inventaire si le joueur le possède."""
        if item in self.inventory:
            self.current_weight = max(0, self.current_weight - item.weight)
            self.inventory.remove(item)

    def find_item(self, name: str):
        """Recherche un objet par son nom (insensible à la casse)."""
        name = name.lower()
        for it in self.inventory:
            if it.name.lower() == name:
                return it
        return None

    def has_item(self, name: str) -> bool:
        """Retourne True si l'objet est présent dans l'inventaire."""
        return self.find_item(name) is not None

    # ============================================================
    # Combat et dégâts
    # ============================================================

    def take_damage(self, amount: int) -> int:
        """
        Reçoit des dégâts en tenant compte de la défense.

        amount : valeur brute.
        Retour : dégâts réellement subis.
        """
        amount = max(0, amount)
        if amount == 0:
            dmg = 0
        else:
            dmg = max(1, amount - self.defense)

        self.hp = max(0, self.hp - dmg)
        return dmg

    def is_alive(self) -> bool:
        """Retourne True si le joueur possède encore des PV."""
        return self.hp > 0

    # ============================================================
    # Historique / Statut
    # ============================================================

    def log(self, message: str):
        """Ajoute un message au journal des événements."""
        self._event_log.append(message)

    def get_history_string(self) -> str:
        """Retourne une version lisible de l’historique du joueur."""
        if not self._event_log:
            return "l'historique est vide."
        lines = ["Historique:"]
        for e in self._event_log:
            lines.append(f"- {e}")
        return "\n".join(lines)

    def get_status_string(self) -> str:
        """Retourne un résumé lisible des statistiques du joueur."""
        return (
            f"{self.name} — PV {self.hp}/{self.max_hp} | "
            f"ATK {self.atk} | DEF {self.defense} | "
            f"Moral {self.moral} | Ressources {self.resources}"
        )
