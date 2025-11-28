"""
ai_quiz.py — Système de mini-quiz IA utilisé en combat.

Ce module gère un ensemble de questions de culture générale et propose
une mécanique de "liaison cognitive" : le joueur doit répondre à une
question, ce qui modifie les dégâts infligés lors d'une attaque.

- Bonne réponse → dégâts * 1.5
- Mauvaise réponse → dégâts * 0.5

Le module enregistre également les statistiques globales des réponses
du joueur, utiles pour afficher son niveau de synchronisation avec l'IA.
"""

import random

# Statistiques globales pour suivre les performances de l'utilisateur
STATS = {
    "correct": 0,
    "wrong": 0,
}

# Banque de questions utilisées par le système IA
QUESTIONS = [
    ("Quel est le nom du plus grand volcan du système solaire ?",
     "Olympus Mons"),
    ("Quel astronaute a été le premier homme à marcher sur la Lune ?",
     "Neil Armstrong"),
    ("Qui est l’auteur du roman de science-fiction « Dune » ?",
     "Frank Herbert"),
    ("Comment s’appelle notre galaxie ?",
     "Voie lactée"),
]


def ask_question(player):
    """
    Pose une question IA au joueur et retourne un multiplicateur de dégâts.

    Retourne :
        1.5 → si la réponse est correcte (coup critique)
        0.5 → si la réponse est incorrecte

    Paramètres :
        player : objet Player, utilisé pour mettre à jour ses statistiques
                 de bonnes/mauvaises réponses.

    Effets :
        - Affiche une question dans le terminal
        - Attend une réponse utilisateur
        - Met à jour STATS et les attributs IA du joueur
    """
    q, ans = random.choice(QUESTIONS)
    print()
    print("🤖 Le système du Vigilant initialise le lien cognitif IA...")
    print()
    print(f"❓ [IA Active] Question : {q}")

    user = input("> ").strip().lower()

    # Bonne réponse → bonus de dégâts
    if user == ans.lower():
        print("✅ Liaison cognitive parfaite. Coup critique 💥 (+50% dégâts)")
        STATS["correct"] += 1
        if player:
            player.ia_correct += 1
        return 1.5

    # Mauvaise réponse → malus de dégâts
    else:
        print(f"❌ Réponse inexacte. L'IA signale : {ans}. (-50% dégâts)")
        STATS["wrong"] += 1
        if player:
            player.ia_wrong += 1
        return 0.5


def get_ai_status(player):
    """
    Retourne un résumé clair des performances IA du joueur.

    Paramètres :
        player : objet Player (non indispensable ici mais conservé pour cohérence)

    Retour :
        - Chaîne décrivant le nombre de bonnes/mauvaises réponses
        - Pourcentage de réussite global
    """
    total = STATS["correct"] + STATS["wrong"]

    if total == 0:
        return "L’IA n’a encore posé aucune question."

    taux = int((STATS["correct"] / total) * 100)

    return (
        f"IA de combat — bonnes réponses : {STATS['correct']}, "
        f"mauvaises : {STATS['wrong']}, "
        f"pourcentage de réussite {taux}%"
    )
