"""
actions.py — Contient toutes les actions réalisables par le joueur.

Ce module regroupe les fonctions principales appelées par l'interpréteur
de commandes du jeu (déplacements, combat, inventaire, interactions PNJ,
utilisation d'objets, etc.).
Les actions interagissent avec l'état du joueur, des salles et du jeu.
"""

from ai_quiz import ask_question, get_ai_status
import player

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
    return game.player.current_room.get_long_description()


def back(game):
    """Permet au joueur de revenir à la salle précédente si possible."""
    if game.in_combat:
        return "❌ Vous ne pouvez pas revenir en arrière pendant un combat."
    if game.player.back():
        return game.player.current_room.get_long_description()
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

def attack(game, enemy_name):
    """Lance un combat contre un ennemi présent dans la salle."""
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

    # Le multiplicateur dépend d'une question IA (système de quiz)
    multiplier = ask_question(game.player)

    base = max(1, game.player.atk - enemy.defense)
    dmg = max(1, int(round(base * multiplier)))
    real = enemy.take_damage(dmg)

    logs = [f"Vous attaquez {enemy.name} et infligez {real} dégâts."]

    # Ennemis vaincus
    if not enemy.is_alive():
        logs.append(f"{enemy.name} est vaincu.\n")
        game.in_combat = False
        game.current_enemy = None

        # Loot
        if enemy.loot:
            for it in enemy.loot:
                if it.name == 'Cristal de propulsion' and game.player.has_crystal:
                    continue
                room.add_item(it)
                logs.append(f"{enemy.name} laisse tomber {it.name}.")
                if it.name == "Cristal de propulsion":
                    game.player.has_crystal = True

        # Boss final du monde 1
        if enemy.is_boss:
            game.player.vorn_defeated = True
            logs.append("Le Capitaine Vorn s'effondre. Les rebelles envahissent la forteresse !")
            if game.player.merchant_sacrifice:
                logs.append(
                    "Dans le chaos, votre équipier sacrifié est libéré. "
                    "Votre moral et votre force augmentent."
                )
                game.player.moral += 3
                game.player.atk += 1

        return "\n".join(logs)

    # Contre-attaque ennemie
    dmg_received = game.player.take_damage(enemy.atk)
    logs.append(f"{enemy.name} riposte et inflige {dmg_received} dégâts.")

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
    """Permet de tuer instantanément un ennemi (cheat)."""
    if not enemy_name:
        return "Cheat sur qui ?"

    room = game.player.current_room
    enemy = room.find_enemy(enemy_name)
    if not enemy:
        return f"Aucun ennemi nommé '{enemy_name}'."
    if not enemy.is_alive():
        return f"{enemy.name} est déjà vaincu."

    enemy.hp = 0
    logs = [f"Vous utilisez le cheat pour tuer instantanément {enemy.name}."]
    logs.append(f"{enemy.name} est vaincu.")

    # Loot éventuel
    if enemy.loot:
        for it in enemy.loot:
            # Cas spécifique : cristal déjà obtenu
            if it.name == 'Cristal de propulsion' and game.player.has_crystal:
                continue
            logs.append(f"{enemy.name} laisse tomber {it.name}.")
            game.player.add_item(it)
            if it.name == "Cristal de propulsion":
                game.player.has_crystal = True

    # Gestion des boss
    if enemy.is_boss:
        # Boss du monde 1 : Capitaine Vorn
        if enemy.name == "Capitaine Vorn":
            game.player.vorn_defeated = True  #Indique que Vorn est mort permet la transition vers le monde 2
            logs.append("Les rebelles envahissent la forteresse !")
            if game.player.merchant_sacrifice:
                logs.append(
                    "Dans le chaos, votre équipier sacrifié est libéré. "
                    "Votre moral et votre force augmentent."
                )
                game.player.moral += 3
                game.player.atk += 1

            logs.append(
                "\nLes réserves de Vorn révèlent assez de minerai pour réparer le Vigilant. "
                "Les rebelles vous aident à préparer le départ d’Eridani Prime."
            )


        # Boss du monde 2 : Gouverneur Karn
        elif enemy.name == "Gouverneur Karn":
            game.player.velyra_karn_defeated = True
            game.player.reputation += 3
            
            
        elif enemy.name == "Seren Taal":
            game.player.ap_taal_dead = True

 
                
                
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
