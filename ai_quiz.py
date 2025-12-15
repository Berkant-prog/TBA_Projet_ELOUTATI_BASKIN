"""
ai_quiz.py — Système de mini-quiz IA utilisé en combat.
"""

import random

STATS = {
    "correct": 0,
    "wrong": 0,
}

QUESTIONS = [
    ("Quel est le nom du plus grand volcan du système solaire ?", "Olympus Mons"),
    ("Quel astronaute a été le premier homme à marcher sur la Lune ?", "Neil Armstrong"),
    ("Qui est l’auteur du roman de science-fiction « Dune » ?", "Frank Herbert"),
    ("Comment s’appelle notre galaxie ?", "Voie lactée"),
]


def get_question():
    """
    Retourne une question et sa réponse attendue.
    """
    return random.choice(QUESTIONS)


def evaluate_answer(player, user_answer, expected_answer):
    """
    Évalue la réponse fournie par le joueur.

    Retourne :
        1.5 si correcte
        0.5 sinon
    """
    if user_answer == expected_answer.lower():
        print("✅ Liaison cognitive parfaite. Coup critique 💥 (+50% dégâts)")
        STATS["correct"] += 1
        if player:
            player.ia_correct += 1
        return 1.5
    else:
        print(f"❌ Réponse inexacte. L'IA signale : {expected_answer}. (-50% dégâts)")
        STATS["wrong"] += 1
        if player:
            player.ia_wrong += 1
        return 0.5


def get_ai_status(player):
    total = STATS["correct"] + STATS["wrong"]
    if total == 0:
        return "L’IA n’a encore posé aucune question."

    taux = int((STATS["correct"] / total) * 100)
    return (
        f"IA de combat — bonnes réponses : {STATS['correct']}, "
        f"mauvaises : {STATS['wrong']}, "
        f"réussite {taux}%"
    )
