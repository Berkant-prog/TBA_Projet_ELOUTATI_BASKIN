# ai_quiz.py
"""Mini-quiz IA pour moduler les dégâts en combat."""

import random

STATS = {
    "correct": 0,
    "wrong": 0,
}

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
    """Pose une question, retourne un multiplicateur de dégâts (0.5, 1.0, 1.5)."""
    q, ans = random.choice(QUESTIONS)
    print()
    print("🤖 Le système du Vigilant initialise le lien cognitif IA...")
    print()
    print(f"❓ [IA Active] Question : {q}")
    user = input("> ").strip().lower()
    if user == ans.lower():
        print("✅ Liaison cognitive parfaite. Coup critique 💥 (+50% dégâts)")
        STATS["correct"] += 1
        if player:
            player.ia_correct += 1
        return 1.5
    else:
        print(f"❌ Réponse inexacte. L'IA signale : {ans}. (-50% dégâts)")
        STATS["wrong"] += 1
        if player:
            player.ia_wrong += 1
        return 0.5

def get_ai_status(player):
    """Résumé des performances IA."""
    total = STATS["correct"] + STATS["wrong"]

    if total == 0:
        return "L’IA n’a encore posé aucune question."

    taux = int((STATS["correct"] / total) * 100)

    return (
        f"IA de combat — bonnes réponses : {STATS['correct']}, "
        f"mauvaises : {STATS['wrong']}, "
        f"pourcentage de réussite {taux}%"
    )

