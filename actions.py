# actions.py
"""
Fonctions d'actions appelées par les commandes.

Chaque fonction prend en premier paramètre une instance de Game.

Fonctions
---------
go(game, direction) -> str
back(game) -> str
look(game) -> str
take(game, item_name) -> str
drop(game, item_name) -> str
check(game) -> str
talk(game, name) -> str
attack(game, enemy_name) -> str
show_help(game) -> str
quit_game(game) -> str
"""

from item import Item


def go(game, direction):
    """Déplacement dans une direction donnée (N, S, E, W, U, D)."""
    if not direction:
        return "Vous devez préciser une direction (N, S, E, W, U, D)."

    direction = direction.upper()
    current = game.player.current_room
    next_room = current.get_exit(direction)

    if next_room is None:
        return "Vous ne pouvez pas aller par là."

    game.player.move_to(next_room)
    desc = next_room.get_long_description()
    hist = game.player.get_history()
    if hist:
        desc += "\n\n" + hist
    return desc


def back(game):
    """Revient au lieu précédemment visité."""
    room = game.player.go_back()
    if room is None:
        return "Vous ne pouvez pas revenir en arrière."
    desc = room.get_long_description()
    hist = game.player.get_history()
    if hist:
        desc += "\n\n" + hist
    return desc


def look(game):
    """Observe l'environnement (description + objets + PNJ + ennemis)."""
    room = game.player.current_room
    desc = room.get_long_description()
    hist = game.player.get_history()
    if hist:
        desc += "\n\n" + hist
    return desc


def take(game, item_name):
    """Prend un objet présent dans la pièce."""
    if not item_name:
        return "Vous devez préciser le nom de l'objet à prendre."

    room = game.player.current_room
    # Cherche l'objet dans la pièce
    for i, item in enumerate(room.inventory):
        if item.name.lower() == item_name.lower():
            # Vérifie le poids
            if not game.player.can_take(item):
                return (
                    f"Vous ne pouvez pas prendre '{item.name}': "
                    "cela dépasserait votre charge maximale."
                )
            room.inventory.pop(i)
            game.player.inventory.append(item)
            # Quête : cristal de propulsion ?
            if item.name.lower() == "cristal de propulsion":
                game.player.has_crystal = True
            return f"Vous avez pris l'objet '{item.name}'."
    return f"L'objet '{item_name}' n'est pas présent ici."


def drop(game, item_name):
    """Dépose un objet depuis l'inventaire dans la pièce."""
    if not item_name:
        return "Vous devez préciser le nom de l'objet à déposer."

    inv = game.player.inventory
    for i, item in enumerate(inv):
        if item.name.lower() == item_name.lower():
            inv.pop(i)
            game.player.current_room.inventory.append(item)
            # Si on dépose le cristal, on garde has_crystal à True ou False ?
            # Ici on considère que la quête est validée dès qu'il a été obtenu.
            return f"Vous avez déposé l'objet '{item.name}'."
    return f"Vous ne possédez pas l'objet '{item_name}'."


def check(game):
    """Affiche le contenu de l'inventaire du joueur."""
    return game.player.get_inventory()


def talk(game, name):
    """Parle à un PNJ dans la pièce courante."""
    if not name:
        return "Vous devez préciser à qui parler (talk <nom>)."

    room = game.player.current_room
    for char in room.characters:
        if char.name.lower() == name.lower():
            return char.get_msg()
    return f"Il n'y a ici aucun personnage nommé '{name}'."


def attack(game, enemy_name):
    """Lance un tour de combat contre un ennemi dans la pièce."""
    if not enemy_name:
        return "Vous devez préciser quel ennemi attaquer (attack <nom>)."

    room = game.player.current_room
    enemy = None
    for e in room.enemies:
        if e.name.lower() == enemy_name.lower():
            enemy = e
            break

    if enemy is None or not enemy.is_alive():
        return f"Aucun ennemi vivant nommé '{enemy_name}' ici."

    lines = []

    # --- Attaque du joueur ---
    enemy.hp -= game.player.atk
    if enemy.hp < 0:
        enemy.hp = 0
    lines.append(
        f"Vous attaquez {enemy.name} et lui infligez {game.player.atk} points de dégâts. "
        f"(PV restants : {enemy.hp})"
    )

    # --- Ennemi mort ? ---
    if not enemy.is_alive():
        lines.append(f"{enemy.name} s'effondre. Il est vaincu.")
        # Loot éventuel
        if enemy.loot is not None:
            room.inventory.append(enemy.loot)
            if enemy.loot.name.lower() == "cristal de propulsion":
                lines.append(
                    "Dans un ultime sursaut, la créature laisse tomber un Cristal de propulsion !"
                )
            else:
                lines.append(
                    f"{enemy.name} laisse tomber '{enemy.loot.name}'."
                )
        return "\n".join(lines)

    # --- Riposte de l'ennemi ---
    dmg = max(1, enemy.atk - game.player.defense)
    game.player.hp -= dmg
    if game.player.hp < 0:
        game.player.hp = 0
    lines.append(
        f"{enemy.name} riposte et vous inflige {dmg} points de dégâts. "
        f"(Vos PV : {game.player.hp})"
    )

    # --- Joueur mort ? ---
    if game.player.hp <= 0:
        lines.append("\nVous succombez à vos blessures. Le Vigilant ne repartira jamais...")
        game.running = False

    return "\n".join(lines)


def show_help(game):
    """Affiche la liste des commandes disponibles."""
    return (
        "Commandes disponibles :\n"
        "- go <dir>   : se déplacer (N, S, E, W, U, D)\n"
        "- back       : revenir en arrière\n"
        "- look       : observer les lieux et les sorties\n"
        "- take <obj> : prendre un objet\n"
        "- drop <obj> : déposer un objet\n"
        "- check      : afficher l'inventaire\n"
        "- talk <pnj> : parler à un personnage\n"
        "- attack <e> : attaquer un ennemi\n"
        "- help       : afficher cette aide\n"
        "- quit       : quitter le jeu"
    )


def quit_game(game):
    """Met fin au jeu."""
    game.running = False
    return "Vous quittez le jeu. Le Vigilant reste en orbite silencieuse..."
