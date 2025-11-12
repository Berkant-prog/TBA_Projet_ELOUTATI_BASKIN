# game.py
# Boucle principale : relie Command, Actions, monde (Rooms), et fins (Win).

from player import Player
from room import Room
from command import Command
from win import Win
from item import Item
from character import Character
from enemy import Enemy
import config
import actions


class Game:
    """Orchestrateur du jeu."""

    def __init__(self):
        self.rooms = {}         # name -> Room
        self.items_catalog = {} # name -> Item (modèle)
        self.pnj_catalog = {}   # name -> Character
        self.enemy_catalog = {} # name -> Enemy (modèle)
        self.player = None
        self.is_running = True
        self.kael_defeated = False

    # ---------- Initialisation ----------
    def start_game(self):
        print(config.INTRO_TEXT.strip())
        self._build_catalogs()
        self._build_world()
        start_room = self.rooms[config.START_ROOM]
        self.player = Player("Orion Vale", starting_room=start_room)
        self.player.current_room = self.rooms[config.START_ROOM]

        print(self.help_text())
        print("\n" + start_room.describe())

    def _build_catalogs(self):
        # Items
        for name, d in config.items_config.items():
            self.items_catalog[name] = Item(
                name=name,
                description=d["description"],
                effect_type=d["effect_type"],
                value=d["value"],
                usable=True
            )
        # PNJ
        for name, d in config.pnj_config.items():
            self.pnj_catalog[name] = Character(
                name=name,
                dialogues=d.get("dialogues", []),
                alignment=d.get("alignment", "neutral"),
                gives_item=d.get("gives_item")
            )
        # Enemies
        for name, d in config.enemies_config.items():
            self.enemy_catalog[name] = Enemy(
                name=name,
                hp=d["hp"],
                atk=d["atk"],
                defense=d["defense"],
                is_boss=d.get("is_boss", False),
                loot=d.get("loot")
            )

    def _clone_item(self, name):
        """Crée une copie indépendante d’un item du catalogue."""
        model = self.items_catalog.get(name)
        if model is None:
            return None
        # On retourne une nouvelle instance identique
        return Item(
            name=model.name,
            description=model.description,
            effect_type=model.effect_type,
            value=model.value,
            usable=model.usable
        )

    def _clone_enemy(self, name):
        """Crée une copie indépendante d’un ennemi (HP propres)."""
        model = self.enemy_catalog.get(name)
        if not model:
            return None
        return Enemy(model.name, model.hp, model.atk, model.defense, model.is_boss, model.loot)

    def _build_world(self):
        """Construit toutes les planètes (Rooms) à partir de config."""
        for rname, d in config.rooms_config.items():
            # ⚠️ Correction ici : on ne rappelle pas deux fois _clone_item()
            items = []
            for n in d.get("items", []):
                clone = self._clone_item(n)
                if clone:
                    items.append(clone)

            pnj = [self.pnj_catalog[n] for n in d.get("pnj", []) if n in self.pnj_catalog]
            enemies = [self._clone_enemy(n) for n in d.get("enemies", []) if self._clone_enemy(n)]

            room = Room(
                name=rname,
                description=d.get("description", ""),
                connected_rooms=d.get("connected_rooms", {}),
                items=items,
                pnj=pnj,
                enemies=enemies
            )

            # Attache une référence temporaire vers player (initialisée après)
            for ch in room.pnj:
                setattr(ch, "_player_ref", None)

            self.rooms[rname] = room

    # ---------- Boucle ----------
    def game_loop(self):
        while self.is_running:
            if self._check_ends():
                break
            raw = input("\n> ")
            cmd = Command(raw)
            cmd.parse()
            try:
                out = cmd.execute(self)
            except Exception as exc:
                out = f"[ERREUR] {type(exc).__name__}: {exc}"
            print(out if out else "(aucune sortie)")
    def do_quitter(self):
        """Quitte le jeu proprement."""
        print("\nFermeture du jeu... Merci d’avoir joué à *Project Vigilant* 🌌")
        exit(0)



    # ---------- Aide ----------
    def help_text(self):
        return (
            "Commandes: explorer | parler <nom> | prendre <objet> | utiliser <objet> | "
            "attaquer <ennemi> | inventaire | historique | aller <direction> | statut | soigner | fuir | quitter"
        )

    # ---------- Wrappers des actions (pour gérer contexte & cohérence) ----------
    def do_explorer(self):
        return actions.explorer(self.player.current_room)

    def do_parler(self, name):
        """Permet de parler à un PNJ présent dans la salle."""
        if not name:
            return "Parler à qui ?"
        return actions.parler(self.player, self.player.current_room, name)



    def do_attaquer(self, name):
        """Permet d’attaquer un ennemi présent dans la salle."""
        if not name:
            return "Attaquer qui ?"
        try:
            return actions.attaquer(self.player, self.player.current_room, name)
        except Exception as e:
            return f"[ERREUR] {type(e).__name__}: {e}"

    def do_explorer(self):
        """Décrit la salle actuelle."""
        if not self.player.current_room:
            return "Erreur : aucune salle actuelle définie."
        return self.player.current_room.describe()

    def do_statut(self):
        """Affiche les stats actuelles du joueur."""
        return self.player.get_status()

    def do_inventaire(self):
        """Affiche l’inventaire du joueur."""
        return self.player.get_inventory()


    def do_prendre(self, item_name):
        if not item_name:
            return "Quel objet prendre ?"
        # Si loot d'un ennemi vient d'être annoncé, il est dans la Room sous forme d'Item catalogué
        # On cherche d'abord dans la salle
        it = self.player.current_room.remove_item(item_name)
        if it:
            self.player.add_item(it)
            self.player.log_event(f"Pris {it.name}")
            return f"Vous prenez {it.name}."
        # Si un PNJ a annoncé de l'aide (gives_item)
        for ch in self.player.current_room.pnj:
            if ch.gives_item and ch.gives_item.lower() == item_name.lower():
                it2 = self._clone_item(ch.gives_item)
                if it2:
                    self.player.add_item(it2)
                    ch.gives_item = None  # ne redonne plus
                    self.player.log_event(f"Reçu de {ch.name}: {it2.name}")
                    return f"{ch.name} vous remet {it2.name}."
        return "Objet introuvable ici."

    def do_utiliser(self, item_name):
        if not item_name:
            return "Utiliser quoi ?"
        res = actions.utiliser(self.player, item_name)
        if "Canon Plasma" in item_name and "ATK" in res:
            self.player.log_event("Armement renforcé (Canon Plasma)")
        return res

    def do_inventaire(self):
        return actions.inventaire(self.player)

    def do_historique(self):
        return actions.historique(self.player)

    def do_aller(self, direction):
        """Déplace le joueur dans la direction indiquée."""
        if not direction:
            return "Aller où ?"

        # Appel à actions.voyager, qui gère le mouvement et renvoie la description du nouveau lieu ou un message d’erreur
        msg = actions.voyager(self.player, self.rooms, direction)

        # Si on a effectivement bougé, rattache le joueur aux PNJ de la nouvelle salle
        if self.player.current_room:
            for ch in self.player.current_room.pnj:
                setattr(ch, "_player_ref", self.player)

        return msg


    def do_soigner(self):
        return actions.soigner(self.player)

    def do_fuir(self):
        """Permet au joueur de fuir le combat en cours."""
        try:
            return actions.fuir_combat(self.player, self.player.current_room)
        except Exception as e:
            return f"[ERREUR] {type(e).__name__}: {e}"


    # ---------- Fins ----------
    def _check_ends(self):
        # Défaite ?
        defeat = Win.check_defeat(self.player)
        if defeat:
            print(Win.show_ending(defeat))
            return True
        # Victoire / Empire ?
        victory = Win.check_victory(self.player)
        if victory:
            print(Win.show_ending(victory))
            return True
        # Fin neutre si Kael vaincu et pas d’autre condition satisfaite
        if self.kael_defeated:
            print(Win.show_ending(Win.check_neutral_end(self.player)))
            return True
        return False


if __name__ == "__main__":   
    g = Game()
    g.start_game()
    g.game_loop()
