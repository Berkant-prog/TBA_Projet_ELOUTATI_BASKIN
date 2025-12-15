"""
actions.py — Contient toutes les actions réalisables par le joueur.

Ce module regroupe les fonctions principales appelées par l'interpréteur
de commandes du jeu (déplacements, combat, inventaire, interactions PNJ,
utilisation d'objets, etc.).
Les actions interagissent avec l'état du joueur, des salles et du jeu.
"""

from ai_quiz import get_question, evaluate_answer, get_ai_status

# ======================
#       DEPLACEMENT
# ======================

def go(game, direction):
    """Permet au joueur d'aller dans une direction donnée s'il est hors combat."""
    if game.in_combat:
        return "❌ Vous ne pouvez pas vous déplacer pendant un combat."
    if not direction:
        return "Indiquez une direction (N, E, S, O, H, B)."

    next_room = game.player.current_room.get_exit(direction)
    if not next_room:
        return "Vous ne pouvez pas aller par là."

    game.player.move_to(next_room)
    print(game.player.current_room.get_long_description())
    return game.player.get_history_string()


def back(game):
    """Permet au joueur de revenir à la salle précédente si possible."""
    if game.in_combat:
        return "❌ Vous ne pouvez pas revenir en arrière pendant un combat."
    if game.player.back():
        print(game.player.current_room.get_long_description())
        return game.player.get_history_string()
    return "Impossible de revenir en arrière."



# ======================
#        OBSERVER
# ======================

def look(game):
    """Retourne une description complète de la salle actuelle."""
    return game.player.current_room.get_long_description()


# ======================
#     GESTION OBJETS
# ======================

def take(game, item_name):
    """Permet au joueur de ramasser un objet présent dans la salle."""
    if not item_name:
        return "Prendre quoi ?"

    room = game.player.current_room
    item = room.find_item(item_name)
    if not item:
        return f"Aucun objet nommé '{item_name}' ici."

    room.remove_item(item)
    game.player.add_item(item)
    return f"Vous prenez {item.name}."


def drop(game, item_name):
    """Permet au joueur de déposer un objet dans la salle."""
    if not item_name:
        return "Déposer quoi ?"

    item = game.player.find_item(item_name)
    if not item:
        return f"Vous ne possédez pas '{item_name}'."

    game.player.remove_item(item)
    game.player.current_room.add_item(item)
    return f"Vous déposez {item.name}."


def inventory(game):
    """Affiche le contenu complet de l'inventaire du joueur, avec poids et limite."""
    if not game.player.inventory:
        return "Votre inventaire est vide."
    lines = ["Inventaire :"]
    lines.append(f"Poids : {game.player.current_weight}")
    lines.append(f"Poids maximum : {game.player.max_weight}")
    lines.append("Objets :")
    for it in game.player.inventory:
        lines.append(f"- {it.name} ({it.weight} kg)")
    return "\n".join(lines)


def check(game, item_name):
    """Affiche la description d'un objet de l'inventaire."""
    if not item_name:
        if not game.player.inventory:
            return "Votre inventaire est vide."
        lines = ["Inventaire :"]
        for it in game.player.inventory:
            lines.append(f"- {it.name}")
        return "\n".join(lines)

    item = game.player.find_item(item_name)

    if item:
        return f"{item.name} : {item.description}"

    lines = [f"'{item_name}' n'est pas dans votre inventaire.", "Inventaire :"]
    for it in game.player.inventory:
        lines.append(f"- {it.name}")
    return "\n".join(lines)


def analyze(game, name):
    """donne la description d'un PNJ dans la salle."""
    if not name:
        return "Analyser qui ?"

    room = game.player.current_room
    target = name.lower()

    # Recherche parmi les PNJ
    for npc in room.characters:
        if npc.name.lower() == target:
            return f"{npc.name} : {npc.description}"


    return f"Il n'y a personne nommé '{name}' ici."



def use(game, item_name):
    """Utilise un objet de l'inventaire (soin, défense ou objet de quête)."""
    if not item_name:
        return "Utiliser quoi ?"

    item = game.player.find_item(item_name)
    if not item:
        return f"Vous ne possédez pas '{item_name}'."

    if not item.usable:
        return f"Vous ne pouvez pas utiliser '{item.name}'."

    # Objet de soin
    if item.effect_type == "heal":
        before = game.player.hp
        game.player.hp = min(game.player.max_hp, before + item.value)
        game.player.remove_item(item)
        return f"Vous utilisez {item.name}. HP : {before} → {game.player.hp}"

    # Bonus de défense
    if item.effect_type == "def":
        before = game.player.defense
        game.player.defense = before + item.value
        game.player.remove_item(item)
        return f"Vous utilisez {item.name}. DEF : {before} → {game.player.defense}"

    # Objet lié à une quête
    if item.effect_type == "quest":
        return f"{item.name} semble important pour votre mission, mais l'utiliser maintenant n'a aucun effet."

    return f"Rien ne se passe lorsque vous utilisez {item.name}."


# ======================
#     INTERACTION PNJ
# ======================

def talk(game, name):
    """Permet au joueur de discuter avec un PNJ présent dans la salle."""
    if not name:
        return "Parler à qui ?"

    room = game.player.current_room
    target = name.lower()

    for npc in room.characters:
        if npc.name.lower() == target:
            return npc.talk(game.player, game)

    return f"Il n'y a personne nommé '{name}' ici."


# ======================
#        COMBAT
# ======================

# Calcul des dégâts infligés par le joueur
# compute_player_damage calcule les dégâts bruts AVANT défense
def _compute_player_damage(player, enemy, multiplier):
    base = max(1, player.atk - enemy.defense)
    return max(1, int(round(base * multiplier)))

# Attaque du joueur
def _player_attack(game, enemy, multiplier):
    dmg = _compute_player_damage(game.player, enemy, multiplier)
    real = enemy.take_damage(dmg)
    return real


# Riposte de l'ennemi
def _enemy_counter_attack(game, enemy):
    return game.player.take_damage(enemy.atk)

# Gestion de la défaite de l'ennemi
def _handle_enemy_defeat(game, enemy, logs): 
    game.in_combat = False
    game.current_enemy = None

    # Loot
    if enemy.loot:
        for it in enemy.loot:
            if it.name == "Cristal de propulsion" and game.player.has_crystal:
                continue
            if it.name == "Cristal de propulsion" and not game.player.has_crystal:
                game.player.has_crystal = True
                game.player.add_item(it)
                logs.append(f"{enemy.name} laisse tomber {it.name}. Vous l'ajoutez à votre inventaire.")
                continue
            game.player.current_room.add_item(it)

            logs.append(f"{enemy.name} laisse tomber {it.name}.")

    # Boss logic
    if enemy.is_boss:
        if enemy.name == "Capitaine Vorn":
            game.player.vorn_defeated = True
            game.player.reputation += 2
            if game.player.merchant_sacrifice:
                game.player.moral += 2
                game.player.atk += 1

        elif enemy.name == "Gouverneur Karn":
            game.player.velyra_karn_defeated = True
            game.player.reputation += 2
            game.player.moral += 1

        elif enemy.name == "Seren Taal":
            game.player.ap_taal_dead = True
            game.player.reputation += 3
            game.player.moral += 2
            
    
    if enemy.name == "Garde Éclaté":
        game.player.moral += 1
        game.player.reputation += 1

# Attaque principale


def attack(game, enemy_name):
    if not enemy_name:
        return "Attaquer qui ?"

    room = game.player.current_room
    enemy = room.find_enemy(enemy_name)
    if not enemy:
        return f"Aucun ennemi nommé '{enemy_name}'."
    if not enemy.is_alive():
        return f"{enemy.name} est déjà vaincu."

    game.in_combat = True
    game.current_enemy = enemy
    logs = []

    # -------------------------------------------------
    #  IA — génération UNIQUE de la question
    # -------------------------------------------------
    if game.current_question is None:
        q, expected = get_question()
        game.current_question = q
        game.current_answer = expected

    print()
    print("🤖 Le système du Vigilant initialise le lien cognitif IA...")
    print()
    print(f"❓ [IA Active] Question : {game.current_question}")

    # -------------------------------------------------
    #  INPUT joueur
    # -------------------------------------------------
    user_input = input("> ").strip().lower()

    # -------------------------------------------------
    #  Commandes info autorisées (SANS consommer la question)
    # -------------------------------------------------
    from command import Command
    cmd = Command(user_input)
    cmd.parse()

    if cmd.verb in (
        "statut", "status", "s",
        "inventaire", "inventory", "i",
        "examiner", "check", "e",
        "utiliser", "use", "u",
        "quit", "exit", "quitter", "q", "b", 
    ):
        return cmd.execute(game)

    # -------------------------------------------------
    #  Évaluation IA (CONSOMME la question)
    # -------------------------------------------------
    multiplier = evaluate_answer(
        game.player,
        user_input,
        game.current_answer
    )

    # La question est consommée
    game.current_question = None
    game.current_answer = None

    # -------------------------------------------------
    #  Attaque joueur (OFFICIELLE)
    # -------------------------------------------------
    real = _player_attack(game, enemy, multiplier)
    logs.append(f"Vous attaquez {enemy.name} et infligez {real} dégâts. (Votre HP : {game.player.hp})")

    if not enemy.is_alive():
        logs.append(f"{enemy.name} est vaincu.\n")
        _handle_enemy_defeat(game, enemy, logs)
        return "\n".join(logs)

    # -------------------------------------------------
    #  Riposte ennemie
    # -------------------------------------------------
    dmg_received = _enemy_counter_attack(game, enemy)
    logs.append(f"{enemy.name} riposte et inflige {dmg_received} dégâts. (HP de l'ennemie : {enemy.hp})")

    if not game.player.is_alive():
        logs.append("Vous êtes mort. Game Over.")
        game.running = False
        game.in_combat = False
        game.current_enemy = None

    return "\n".join(logs)





# ======================
#   Cheat provispoire
# ======================
def cheat(game, enemy_name):
    """Tue instantanément un ennemi (outil de debug)."""

    if not enemy_name:
        return "Cheat sur qui ?"

    room = game.player.current_room
    enemy = room.find_enemy(enemy_name)

    if not enemy:
        return f"Aucun ennemi nommé '{enemy_name}'."
    if not enemy.is_alive():
        return f"{enemy.name} est déjà vaincu."

    logs = [f"[CHEAT] {enemy.name} est éliminé instantanément."]

    # Simule un combat propre
    game.in_combat = True
    game.current_enemy = enemy

    # Tue l’ennemi
    enemy.hp = 0

    # Reset combat
    game.in_combat = False
    game.current_enemy = None
    game.current_question = None
    game.current_answer = None

    return "\n".join(logs)


# ======================
#     INFORMATIONS
# ======================

def status(game):
    """Retourne l'état complet du joueur (HP, ATK, DEF, moral, poids, etc.)."""
    return game.player.get_status_string()


def history(game):
    """Retourne l'historique des actions importantes effectuées par le joueur."""
    return game.player.get_history_string()


def ai_status(game):
    """Retourne l'état actuel du module IA (quiz / bonus)."""
    return get_ai_status(game.player)


# ======================
#       SYSTEME
# ======================

def quit_game(game):
    """Stoppe la boucle principale du jeu et quitte la partie."""
    game.running = False
    return "Fermeture du jeu..."
