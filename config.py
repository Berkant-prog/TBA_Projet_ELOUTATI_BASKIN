# config.py
# Fichier de configuration : données du monde, des PNJ, objets, et planètes.

# Texte d’introduction
INTRO_TEXT = """
En 2239, le vaisseau Vigilant, conçu par l'ESIEE, quitte la Terre pour sauver l'humanité...
"""

# Salle de départ
START_ROOM = "Eridani Prime"

# Configuration des planètes / rooms
rooms_config = {
    # Exemple :
    # "Eridani Prime": {
    #     "description": "...",
    #     "connected_rooms": {"est": "Velyra IX"},
    #     "pnj": ["Yara"],
    #     "items": ["Canon Plasma"]
    # }
}

# Objets disponibles
items_config = {
    # "Canon Plasma": {"effect_type": "atk", "value": 5}
}

# Ennemis
enemies_config = {
    # "Capitaine Vorn": {"hp": 60, "atk": 12, "defense": 4, "is_boss": True}
}

# Conditions de victoire/défaite
win_conditions = {
    # "victory": {"moral_min": 60, "reputation_min": 50},
    # "defeat": {"hp": 0, "energie": 0}
}

