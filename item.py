# item.py
"""
Classe Item : représente un objet manipulable par le joueur.

Attributs
---------
name : str
    Nom de l'objet.
description : str
    Description courte.
weight : int | float
    Poids de l'objet en kg.

Méthodes
--------
__str__() -> str
    Représentation textuelle de l'objet.
"""

class Item:
    """Objet que le joueur peut prendre, porter, déposer."""

    def __init__(self, name, description, weight):
        self.name = name
        self.description = description
        self.weight = weight

    def __str__(self):
        return f"{self.name} : {self.description} ({self.weight} kg)"
