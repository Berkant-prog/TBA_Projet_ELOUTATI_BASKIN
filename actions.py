# actions.py
"""Command callbacks — clean, stable, IA integrated."""

from ai_quiz import ask_question, get_ai_status


def go(game, direction):
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
    if game.in_combat:
        return "❌ Vous ne pouvez pas revenir en arrière pendant un combat."
    if game.player.back():
        return game.player.current_room.get_long_description()
    return "Impossible de revenir en arrière."


def look(game):
    return game.player.current_room.get_long_description()


def take(game, item_name):
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
    if not item_name:
        return "Déposer quoi ?"

    item = game.player.find_item(item_name)
    if not item:
        return f"Vous ne possédez pas '{item_name}'."

    game.player.remove_item(item)
    game.player.current_room.add_item(item)
    return f"Vous déposez {item.name}."


def inventory(game):
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


def use(game, item_name):
    if not item_name:
        return "Utiliser quoi ?"

    item = game.player.find_item(item_name)
    if not item:
        return f"Vous ne possédez pas '{item_name}'."

    if not item.usable:
        return f"Vous ne pouvez pas utiliser '{item.name}'."

    if item.effect_type == "heal":
        before = game.player.hp
        game.player.hp = min(game.player.max_hp, before + item.value)
        game.player.remove_item(item)
        return f"Vous utilisez {item.name}. HP : {before} → {game.player.hp}"

    if item.effect_type == "def":
        before = game.player.defense
        game.player.defense = before + item.value
        game.player.remove_item(item)
        return f"Vous utilisez {item.name}. DEF : {before} → {game.player.defense}"

    if item.effect_type == "quest":
        return f"{item.name} semble important pour votre mission, mais l'utiliser maintenant n'a aucun effet."

    return f"Rien ne se passe lorsque vous utilisez {item.name}."


def talk(game, name):
    if not name:
        return "Parler à qui ?"

    room = game.player.current_room
    target = name.lower()

    for npc in room.characters:
        if npc.name.lower() == target:
            return npc.talk(game.player, game)

    return f"Il n'y a personne nommé '{name}' ici."


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

    multiplier = ask_question(game.player)

    base = max(1, game.player.atk - enemy.defense)
    dmg = max(1, int(round(base * multiplier)))
    real = enemy.take_damage(dmg)

    logs = [f"Vous attaquez {enemy.name} et infligez {real} dégâts."]

    if not enemy.is_alive():
        logs.append(f"{enemy.name} est vaincu.")
        game.in_combat = False
        game.current_enemy = None

        if enemy.loot:
            for it in enemy.loot:
                if it.name == 'Cristal de propulsion' and game.player.has_crystal:
                    continue
                room.add_item(it)
                logs.append(f"{enemy.name} laisse tomber {it.name}.")
                if it.name == "Cristal de propulsion":
                    game.player.has_crystal = True

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

    dmg_received = game.player.take_damage(enemy.atk)
    logs.append(f"{enemy.name} riposte et inflige {dmg_received} dégâts.")

    if not game.player.is_alive():
        logs.append("Vous êtes mort. Game Over.")
        game.running = False
        game.in_combat = False
        game.current_enemy = None

    return "\n".join(logs)


def status(game):
    return game.player.get_status_string()


def history(game):
    return game.player.get_history_string()


def ai_status(game):
    return get_ai_status(game.player)


def quit_game(game):
    game.running = False
    return "Fermeture du jeu..."
