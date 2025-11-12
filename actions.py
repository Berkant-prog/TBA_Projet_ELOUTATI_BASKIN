# actions.py
# Contient toutes les fonctions d'action (combat, soins, interactions, etc.)

def attaquer(player, room, target_name):
    """Gère un combat entre le joueur et un ennemi dans la salle."""
    # Vérifie la présence de l'ennemi
    enemy = None
    for e in room.enemies:
        if e.name.lower() == target_name.lower():
            enemy = e
            break
    if not enemy:
        return "Aucun ennemi de ce nom ici."

    # Combat : joueur attaque
    dmg_to_enemy = max(0, player.atk - enemy.defense)
    enemy.hp = max(0, enemy.hp - dmg_to_enemy)
    player.log_event(f"{player.name} attaque {enemy.name} et inflige {dmg_to_enemy} dégâts.")
    msg = f"{player.name} attaque {enemy.name} et inflige {dmg_to_enemy} dégâts.\n"

    # Vérifie si l'ennemi est mort
    if not enemy.is_alive():
        msg += f"{enemy.name} s'effondre !\n"
        loot = enemy.drop_loot()
        room.enemies.remove(enemy)
        if loot:
            msg += f"Vous trouvez un objet : {loot}.\n"
            player.log_event(f"Reçu butin : {loot}")
            # Ajoute le butin à la salle
            if hasattr(room, "items"):
                room.items.append(loot)
        else:
            msg += "Aucun butin trouvé.\n"
        return msg

    # Si l'ennemi est encore vivant : riposte
    dmg_to_player = max(0, enemy.atk - player.defense)
    player.hp = max(0, player.hp - dmg_to_player)
    player.log_event(f"{enemy.name} riposte et inflige {dmg_to_player} dégâts à {player.name}.")
    msg += f"{enemy.name} riposte et inflige {dmg_to_player} dégâts à {player.name}."
    return msg



def parler(player, room, name):
    """Dialogue avec un PNJ s’il est présent dans la pièce."""
    for ch in room.pnj:
        if ch.name.lower() == name.lower():
            text = ch.talk(player)  # ✅ on passe le joueur
            player.log_event(f"Parlé avec {ch.name}")
            return text
    return "Personne de ce nom ici."


def utiliser(player, item_name):
    """Utilise un objet de l’inventaire."""
    if not player.inventory:
        return "Votre inventaire est vide."
    return player.use_item(item_name)


def soigner(player):
    """Soigne le joueur avec une trousse médicale si disponible."""
    heal_item = None
    for it in player.inventory:
        if it.effect_type == "hp":
            heal_item = it
            break
    if not heal_item:
        return "Aucune trousse médicale dans l’inventaire."
    player.hp = min(player.max_hp, player.hp + heal_item.value)
    player.inventory.remove(heal_item)
    return f"Vous utilisez {heal_item.name} et regagnez {heal_item.value} PV."


def prendre(player, room, item_name):
    """Permet au joueur de ramasser un objet."""
    item = room.remove_item(item_name)
    if not item:
        return f"Aucun objet nommé {item_name} ici."
    player.add_item(item)
    return f"Vous prenez {item.name}."


def inventaire(player):
    """Affiche l’inventaire du joueur."""
    if not player.inventory:
        return "Inventaire vide."
    text = "Inventaire :\n"
    for it in player.inventory:
        text += f"- {it.name} ({it.effect_type}+{it.value})\n"
    return text.strip()


def statut(player):
    """Affiche les statistiques du joueur."""
    return player.get_status()


def fuir_combat(player, room):
    """Permet au joueur de fuir le combat en cours, si des ennemis sont présents."""
    if not room.enemies:
        return "Rien dont fuir."

    # On suppose que le joueur fuit tous les ennemis de la salle
    ennemis = ", ".join(e.name for e in room.enemies if e.is_alive())
    if not ennemis:
        return "Aucun ennemi vivant à fuir."

    # Effets sur le joueur
    player.energie = max(0, player.energie - 10)
    player.moral = max(0, player.moral - 5)
    player.log_event(f"Fuite du combat face à {ennemis}")

    # Narration
    return f"Vous battez en retraite, échappant à {ennemis}. Votre énergie et votre moral baissent légèrement."




def historique(player):
    return player.get_history()

def voyager(player, rooms, direction):
    current = player.current_room
    if not current or direction not in current.connected_rooms:
        return "Impossible d'aller par là."
    dest_name = current.connected_rooms[direction]
    new_room = rooms.get(dest_name)
    if not new_room:
        return "Destination inconnue."
    player.current_room = new_room
    player.log_event(f"Voyage vers {new_room.name}.")
    return new_room.describe()

