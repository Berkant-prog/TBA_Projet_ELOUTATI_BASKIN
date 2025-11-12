# config.py
# Fichier de configuration : univers, PNJ, ennemis, objets et planètes du jeu.

# -----------------------------------------------------------
# Introduction
# -----------------------------------------------------------

INTRO_TEXT = """
En 2239, l'ESIEE lance le vaisseau interstellaire 'Vigilant' pour trouver un monde habitable.
Une onde gravitationnelle inconnue projette l'appareil vers un système lointain.
Réparez le Vigilant, ralliez des alliés, et décidez du destin de l'humanité.
"""

START_ROOM = "Eridani Prime"

# -----------------------------------------------------------
# Objets du jeu
# -----------------------------------------------------------

# effect_type ∈ {"atk", "def", "hp", "energie", "moral", "reputation", "key"}
items_config = {
    "Canon Plasma": {
        "description": "Arme lourde issue du module minier, améliore la puissance de feu.",
        "effect_type": "atk",
        "value": 5
    },
    "Bouclier Résonance": {
        "description": "Bouclier énergétique expérimental conçu à l'ESIEE.",
        "effect_type": "def",
        "value": 5
    },
    "Trousse Médicale": {
        "description": "Kit de premiers secours utilisé par les équipes d’exploration.",
        "effect_type": "hp",
        "value": 25
    },
    "Noyau d'Énergie": {
        "description": "Module d’énergie utilisé pour ravitailler le réacteur du Vigilant.",
        "effect_type": "energie",
        "value": 10
    },
    "Clé Astrale": {
        "description": "Artefact mystique ouvrant des portails vers d'autres mondes.",
        "effect_type": "reputation",
        "value": 10
    }
}

# -----------------------------------------------------------
# PNJ non hostiles
# -----------------------------------------------------------

pnj_config = {
    "Yara": {
        "alignment": "ally",
        "dialogues": [
            "La liberté ne s’octroie pas, elle se gagne.",
            "Si on sauve des civils, on sauve notre humanité."
        ],
        "gives_item": "Bouclier Résonance"
    },
    "Tzenn": {
        "alignment": "ally",
        "dialogues": [
            "J'ai vu des empires naître, mourir... et se répéter.",
            "Le calcul sans empathie conduit à la tyrannie."
        ],
        "gives_item": "Noyau d'Énergie"
    },
    "Zekh": {
        "alignment": "neutral",
        "dialogues": [
            "Réveille-les... mais sois prêt à porter leur souffrance.",
            "La vérité blesse, l’illusion rassure."
        ],
        "gives_item": "Clé Astrale"
    }
}

# -----------------------------------------------------------
# Ennemis
# -----------------------------------------------------------

enemies_config = {
    "Capitaine Vorn": {
        "hp": 60,
        "atk": 12,
        "defense": 4,
        "is_boss": True,
        "loot": "Canon Plasma"
    },
    "Drone MK-V": {
        "hp": 80,
        "atk": 14,
        "defense": 6,
        "is_boss": False,
        "loot": "Noyau d'Énergie"
    },
    "Gardien Spectral": {
        "hp": 100,
        "atk": 15,
        "defense": 8,
        "is_boss": True,
        "loot": "Clé Astrale"
    },
    "Général Kael": {
        "hp": 150,
        "atk": 18,
        "defense": 10,
        "is_boss": True,
        "loot": None
    }
}

# -----------------------------------------------------------
# Planètes / Rooms
# -----------------------------------------------------------

rooms_config = {
    "Eridani Prime": {
        "description": "Monde minier opprimé. Cieux rouges, tunnels poussiéreux, population en révolte.",
        "connected_rooms": {"est": "Velyra IX"},
        "pnj": ["Yara"],
        "enemies": ["Capitaine Vorn"],
        "items": ["Trousse Médicale"]
    },
    "Velyra IX": {
        "description": "Planète-machine. Tours de données et IA dormantes sous les vents métalliques.",
        "connected_rooms": {"ouest": "Eridani Prime", "est": "Lumae Delta"},
        "pnj": ["Tzenn"],
        "enemies": ["Drone MK-V"],
        "items": []
    },
    "Lumae Delta": {
        "description": "Océan de brume. Temple holographique, chants d'esprits numériques.",
        "connected_rooms": {"ouest": "Velyra IX", "est": "Kaos-7"},
        "pnj": ["Zekh"],
        "enemies": ["Gardien Spectral"],
        "items": []
    },
    "Kaos-7": {
        "description": "Forteresse volcanique. Dernier bastion de la Fédération Humaine corrompue.",
        "connected_rooms": {"ouest": "Lumae Delta"},
        "pnj": [],
        "enemies": ["Général Kael"],
        "items": []
    }
}

# -----------------------------------------------------------
# Conditions de victoire et de défaite
# -----------------------------------------------------------

win_conditions = {
    "renaissance": {"moral_min": 61, "reputation_min": 51},  # fin héroïque
    "empire": {"moral_max": 39, "reputation_max": 29},       # fin tyrannique
    "derive": {"hp_max": 0, "energie_max": 19}               # mort ou dérive
}
