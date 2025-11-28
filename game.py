"""
game.py — Moteur principal du jeu "Vigilant : Chapitre I — Eridani Prime".

Ce module gère :
- la construction du monde (rooms, PNJ, ennemis, objets),
- l’introduction narrative et les choix initiaux du joueur,
- l’état global du jeu (combat, running, ennemi courant),
- la boucle principale d’interaction,
- l’exécution des commandes via Command.

Il s’agit de la classe centrale du jeu (le "Game Manager").
"""

from room import Room
from item import Item
from enemy import Enemy
from character import Character
from player import Player
from command import Command


class Game:
    """
    Classe principale orchestrant tout le jeu.

    Attributs :
        rooms (dict[str, Room]) : toutes les zones explorables.
        player (Player) : le joueur courant.
        in_combat (bool) : indique si un combat est en cours.
        current_enemy (Enemy|None) : ennemi affronté pendant un combat.
        running (bool) : contrôle la boucle principale du jeu.

    L’initialisation lance automatiquement :
        - la construction du monde,
        - l’introduction + le choix dramatique du crash.
    """

    def __init__(self):
        """Initialise le jeu, construit les rooms et lance l’intro."""
        self.rooms = {}
        self.player = None
        self.in_combat = False
        self.current_enemy = None
        self.running = True

        self._build_world()
        self._intro_and_crash()

    # =========================================================
    #   WORLD BUILDING — Construction de l’univers narratif
    # =========================================================

    def _build_world(self):
        """
        Crée toutes les pièces (rooms), leurs descriptions, connexions,
        objets, PNJ et ennemis.

        C’est le “setup” narratif et spatial du Chapitre I :
        - Eridani Prime
        - Avant-poste minier
        - Marché labyrinthique
        - Cité-forteresse

        Chaque room est connectée Est/Ouest en ligne droite.
        """
        # Rooms
        eridani = Room(
            "Eridani Prime",
            "dans un district pauvre, des fumées noires s’élèvent au-dessus des toits. "
            "Des affiches de propagande couvrent les murs. "
            "Les habitants avancent avec un mélange de peur et de résignation."
        )
        avant_poste = Room(
            "Avant-poste minier",
            "au milieu d’échafaudages branlants, de gardes épuisés et de mineurs au regard vide. "
            "L’air est lourd de poussière et d’électricité."
        )
        marche = Room(
            "Marché labyrinthique",
            "un dédale d’allées étroites, d’échoppes sombres et de murmures étouffés. "
            "Les hommes de main de Vorn rôdent à chaque coin d’ombre."
        )
        forteresse = Room(
            "Cité-forteresse",
            "des tours massives, des projecteurs écarlates et des soldats patrouillant sans relâche. "
            "C’est ici que le Capitaine Vorn impose son règne."
        )

        # Connexions spatiales en ligne Est/Ouest
        eridani.connect(avant_poste, "E")
        avant_poste.connect(marche, "E")
        marche.connect(forteresse, "E")

        # Stockage des rooms
        self.rooms = {
            "Eridani Prime": eridani,
            "Avant-poste minier": avant_poste,
            "Marché labyrinthique": marche,
            "Cité-forteresse": forteresse,
        }

        # Objet initial (trousse de soin)
        medkit = Item(
            "Trousse Médicale",
            "Une trousse de soin rudimentaire (+25 PV).",
            effect_type="heal",
            value=25,
            usable=True,
            weight=3,
        )
        avant_poste.add_item(medkit)

        # ------------------------------
        #  PNJ — dialogues et callbacks
        # ------------------------------

        # Ralen
        ralen = Character(
            "Ralen",
            "Un citoyen au regard vif malgré les cendres sur son visage."
        )

        def talk_ralen(player, game, self_char):
            """Dialogue dynamique selon si le joueur l’a déjà rencontré."""
            if not player.met_ralen:
                player.met_ralen = True
                player.log("Vous avez rencontré Ralen à Eridani Prime.")
                return (
                    "Ralen : Vous n’avez pas l’air d’ici... "
                    "Si vous voulez comprendre ce qui se passe, suivez la route vers l’est. "
                    "Les mineurs de l’avant-poste vous diront le reste."
                )
            else:
                return "Ralen : L’est vous attend toujours. Les mines, puis le marché... Et enfin Vorn."

        ralen.on_talk = talk_ralen
        eridani.add_character(ralen)

        # Ingénieur Malek
        malek = Character(
            "Ingénieur Malek",
            "Un technicien nerveux qui tente de réparer une foreuse brisée."
        )

        def talk_malek(player, game, self_char):
            """Dialogue variant selon les ressources du joueur."""
            if player.resources >= 3:
                return (
                    "Malek : Vous avez du matériel ? Parfait. "
                    "Je peux stabiliser les forages et calmer les gardes. "
                    "Au marché, on murmure qu’un marchand détient un Cristal de propulsion."
                )
            else:
                return (
                    "Malek : Sans ressources, les gardes ne vous laisseront pas faire. "
                    "Vous devrez sans doute vous salir les mains... ou négocier au marché."
                )

        malek.on_talk = talk_malek
        avant_poste.add_character(malek)

        # Marchand — choix moral central
        marchand = Character(
            "Marchand",
            "Un homme sec, aux yeux calculateurs, entouré de caisses verrouillées."
        )

        def talk_marchand(player, game, self_char):
            """
            Dialogue crucial : le marchand propose d'échanger
            un membre d’équipage contre le Cristal de propulsion.
            """
            if player.merchant_deal_done:
                if player.merchant_sacrifice:
                    return "Marchand : Les affaires sont les affaires. Profitez bien de votre cristal."
                if player.merchant_refused:
                    return "Marchand : Vous avez refusé. Je ne traite plus avec vous."
                # Version neutre conservée en commentaire

            print(
                "Marchand : J'ai un Cristal de propulsion.\n"
                "Mais je ne l’échange pas contre de l’argent.\n\n"
                "Je veux un membre de votre équipage.\n"
                "Il travaillera pour moi. C’est le prix.\n\n"
                "1️⃣ Accepter l’échange (cristal + ressources, moral ↓)\n"
                "2️⃣ Refuser (rencontre avec Yara)\n"
            )
            choix = input("> ").strip()
            if choix == "1":
                player.merchant_deal_done = True
                player.merchant_sacrifice = True
                player.moral -= 3
                player.resources += 2

                # Donne le cristal si le joueur ne l’a pas déjà
                if not player.has_crystal:
                    cristal = Item(
                        "Cristal de propulsion",
                        "Cristal énergétique indispensable à la réparation du Vigilant.",
                        effect_type="quest",
                        value=0,
                        usable=False,
                        weight=2,
                    )
                    player.add_item(cristal)
                    player.has_crystal = True

                return (
                    "Le marchand sourit et fait emmener un membre de votre équipage.\n"
                    "Vous obtenez le Cristal… mais à quel prix ?"
                )
            else:
                player.merchant_deal_done = True
                player.merchant_refused = True
                player.met_yara = True
                player.moral += 1
                return (
                    "Vous refusez net.\n"
                    "Dans une ruelle sombre, une femme encapuchonnée vous observe...\n"
                    "Yara : « Tu as refusé de vendre les tiens. On doit parler. »"
                )

        marchand.on_talk = talk_marchand
        marche.add_character(marchand)

        # Yara (rebelle)
        yara = Character(
            "Yara",
            "Une femme encapuchonnée, regard déterminé, symbole rebelle au poignet."
        )

        def talk_yara(player, game, self_char):
            """Dialogue change selon progression (rencontre + boss vaincu)."""
            if not player.met_yara:
                return "Une silhouette encapuchonnée passe fugacement, puis disparaît."
            if not player.vorn_defeated:
                return (
                    "Yara : Tu as gardé ton équipage. Bien.\n"
                    "Nous préparons un assaut sur la forteresse. "
                    "Abats Vorn, et nous t’aiderons à quitter cette planète."
                )
            else:
                return (
                    "Yara : Vorn est tombé grâce à toi. "
                    "Quand ton vaisseau sera prêt, Eridani se souviendra de ton nom."
                )

        yara.on_talk = talk_yara
        marche.add_character(yara)

        # Ennemis
        patrouilleur = Enemy("Patrouilleur de Vorn", hp=40, atk=7, defense=2)
        avant_poste.add_enemy(patrouilleur)

        # Boss final
        vorn = Enemy(
            "Capitaine Vorn",
            hp=85,
            atk=12,
            defense=4,
            is_boss=True,
            loot=[
                Item(
                    "Cristal de propulsion",
                    "Cristal capturé dans les réserves de Vorn.",
                    effect_type="quest",
                    value=0,
                    usable=False,
                    weight=2,
                )
            ],
        )
        forteresse.add_enemy(vorn)

    # =========================================================
    #   INTRODUCTION + CHOIX DRAMATIQUE DU CRASH
    # =========================================================

    def _intro_and_crash(self):
        """
        Affiche l’introduction narrative et demande au joueur
        de faire un choix moral déterminant :
            - sauver l’équipage,
            - ou sauver les ressources.

        Ce choix modifie les statistiques du joueur
        et oriente sa relation au monde.
        """
        print("En 2239, l'ESIEE lance le vaisseau interstellaire 'Vigilant' pour trouver un monde habitable.")
        print("Une onde gravitationnelle inconnue projette l'appareil vers un système lointain.")
        print("Réparez le Vigilant, ralliez des alliés, et décidez du destin de l'humanité.\n")

        name = input("Entrez le nom de votre capitaine (laisser vide pour 'Orion Vale') : ").strip()
        if not name:
            name = "Orion Vale"

        start_room = self.rooms["Eridani Prime"]
        self.player = Player(name, start_room)

        print("\n🌌 CHAPITRE I — ERIDANI PRIME 🌌")
        print("Vous vous réveillez dans un caisson cryo… Le Vigilant tremble… Un crash est imminent.\n")

        print("🔥 Le crash est inévitable. Vous devez faire un choix :")
        print("1️⃣ Sauver tout l'équipage (moral +2, attaque +1, ressources −2)")
        print("2️⃣ Sauver les ressources (défense +3, ressources +2, moral −2)")

        choix = ""
        while choix not in ("1", "2"):
            choix = input("> ").strip()

        # Le traducteur (toujours donné, mais interprété différemment)
        translator = Item(
            "Puce neuronale traductrice",
            "Implant qui traduit en temps réel les langues d’Eridani.",
            effect_type="quest",
            value=0,
            usable=False,
            weight=1,
        )
        self.player.add_item(translator)
        self.player.has_translator = True

        # Effets du choix initial
        if choix == "1":
            self.player.moral += 2
            self.player.atk += 1
            self.player.resources = max(0, self.player.resources - 2)
            print("\nVous arrachez des survivants des flammes… mais perdez une partie du matériel vital.")
            print("➡️ Un membre d’équipage utilise sa puce neuronale traductrice.\n")
        else:
            self.player.defense += 3
            self.player.resources += 4
            self.player.moral -= 2

            # Objet bonus propre à ce choix
            module = Item(
                "Module d'énergie stabilisé",
                "Un module récupéré intact dans les soutes. "
                "Il améliore la stabilité du réacteur portable (+2 DEF lorsqu'utilisé).",
                effect_type="def",
                value=2,
                usable=True,
                weight=2,
            )
            self.player.add_item(module)

            print("\nVous scellez les compartiments pleins d’équipage pour sauver les soutes.")
            print("\nCependant, il vous reste quelques survivants.")
            print("➡️ La puce neuronale d’un officier vous sert désormais de traducteur.")
            print("➡️ Vous récupérez des modules, de l’énergie et des pièces intactes…")
            print("➡️ Vous récupérez un Module d'énergie stabilisé dans les décombres.\n")

        # Affichage de la room initiale et de l’aide
        print(self.player.current_room.get_long_description())
        print(self.help_text() + "\n")

    # =========================================================
    #   HELP TEXT — Commandes disponibles
    # =========================================================

    def help_text(self):
        """Retourne la liste des commandes disponibles pour affichage permanent."""
        return (
            "Commandes disponibles :\n"
            "g : aller <direction> | retour | o : observer | p : prendre <objet> | j : jeter <objet> | i : inventaire | e : examiner <objet> |\n"
            "t : parler <nom> | a : attaquer <ennemi> | u : utiliser <objet> | s : statut | h : historique | ia | q : quitter"
        )

    # =========================================================
    #   MAIN LOOP — Boucle de jeu
    # =========================================================

    def play(self):
        """
        Lance la boucle principale du jeu :
        - lit une commande utilisateur,
        - la transmet à Command(),
        - affiche le résultat,
        - puis réaffiche l’aide.

        La boucle continue tant que self.running == True.
        """
        while self.running:
            try:
                cmd_line = input("> ")
            except EOFError:
                break

            cmd = Command(cmd_line)
            output = cmd.execute(self)

            if output:
                print(output)

            # Affiche toujours les commandes après chaque action
            print("\n" + self.help_text() + "\n")


# Point d’entrée du programme
if __name__ == "__main__":
    g = Game()
    g.play()
