# player.py
"""Player class: stats, inventory, movement history, quest flags."""

class Player:
    def __init__(self, name: str, start_room):
        self.name = name

        # Basic stats
        self.hp = 100
        self.max_hp = 100
        self.atk = 8
        self.defense = 3
        self.moral = 0
        self.resources = 0
        

        # Inventory
        self.inventory = []
        self.max_weight = 20  # max carry weight
        self.current_weight = 0

        # Position & history
        self.current_room = start_room
        self._room_history = []   # stack of previous rooms
        self._event_log = []      # textual history

        # Quest / story flags
        self.has_translator = False
        self.has_crystal = False

        self.merchant_deal_done = False
        self.merchant_sacrifice = False
        self.merchant_refused = False

        self.met_yara = False
        self.met_ralen = False
        self.vorn_defeated = False
        
        # IA stats
        self.ia_correct = 0
        self.ia_wrong = 0
        self.ia_questions_answered = 0


    # --- Movement ---

    def move_to(self, new_room):
        if self.current_room is not None:
            self.log(f"Vous êtes allé de {self.current_room.name} à {new_room.name}.")
            self._room_history.append(self.current_room)
        self.current_room = new_room

    def back(self):
        """Go back to previous room, if any. Returns True/False."""
        if not self._room_history:
            return False
        self.current_room = self._room_history[len(self._room_history) - 1]
        self.log(f"Vous êtes retourné en arrière à {self.current_room.name}.")
        return True

    # --- Inventory ---

    def add_item(self, item):
        self.current_weight += item.weight
        self.inventory.append(item)

    def remove_item(self, item):
        if item in self.inventory:
            self.current_weight = max(0, self.current_weight - item.weight)
            self.inventory.remove(item)

    def find_item(self, name: str):
        name = name.lower()
        for it in self.inventory:
            if it.name.lower() == name:
                return it
        return None

    def has_item(self, name: str) -> bool:
        return self.find_item(name) is not None

    # --- Damage system ---

    def take_damage(self, amount: int) -> int:
        """Receive damage reduced by defense. Minimum 1 if amount>0."""
        amount = max(0, amount)
        if amount == 0:
            dmg = 0
        else:
            dmg = max(1, amount - self.defense)

        self.hp = max(0, self.hp - dmg)
        return dmg

    def is_alive(self) -> bool:
        return self.hp > 0

    # --- Logs / status ---

    def log(self, message: str):
        self._event_log.append(message)

    def get_history_string(self) -> str:
        if not self._event_log:
            return "l'historique est vide."
        lines = ["Historique:"]
        for e in self._event_log:
            lines.append(f"- {e}")
        return "\n".join(lines)

    def get_status_string(self) -> str:
        return (
            f"{self.name} — PV {self.hp}/{self.max_hp} | "
            f"ATK {self.atk} | DEF {self.defense} | "
            f"Moral {self.moral} | Ressources {self.resources}"
        )
