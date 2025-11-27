# item.py
"""Items that can be found or used by the player."""

class Item:
    def __init__(
        self,
        name: str,
        description: str,
        effect_type: str = "misc",
        value: int = 0,
        usable: bool = False,
        weight: int = 1,
    ):
        self.name = name
        self.description = description
        self.effect_type = effect_type  # "heal", "quest", etc.
        self.value = value
        self.usable = usable
        self.weight = weight

    def __str__(self):
        return f"{self.name}: {self.description} ({self.weight} kg)"
