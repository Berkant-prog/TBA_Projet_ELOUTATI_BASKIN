# character.py
"""Non-player characters (NPCs)."""

class Character:
    def __init__(self, name: str, description: str, messages=None):
        self.name = name
        self.description = description
        self.messages = messages or []
        self._msg_index = 0

        # Optional callback: on_talk(player, game, self)
        self.on_talk = None

    def talk(self, player, game=None):
        """Return what the NPC says."""
        if callable(self.on_talk):
            return self.on_talk(player, game, self)

        if not self.messages:
            return f"{self.name} reste silencieux."

        msg = self.messages[self._msg_index]
        self._msg_index = (self._msg_index + 1) % len(self.messages)
        return f"{self.name}: {msg}"

    def __str__(self):
        return f"{self.name}: {self.description}"
