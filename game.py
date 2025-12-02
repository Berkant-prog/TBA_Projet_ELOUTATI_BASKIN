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

import random
import actions
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

        self._build_world_1()
        self._intro_and_crash()

    # =========================================================
    #   WORLD BUILDING — Construction de l’univers narratif
    # =========================================================

    def _build_world_1(self):
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
        
        # Assignation du game aux rooms
        for r in (eridani, avant_poste, marche, forteresse):
            r.game = self

        
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
        #cristal de propulsion obtenu plus tard dans le jeu   
        cristal = Item(
                        "Cristal de propulsion",
                        "Cristal énergétique indispensable à la réparation du Vigilant.",
                        effect_type="quest",
                        value=0,
                        usable=False,
                        weight=2,
                    )
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

                # Donne le cristal si le joueur ne l’a pas déjà (cas théorique)
                if not player.has_crystal:
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
            hp=80,
            atk=12,
            defense=4,
            is_boss=True,
            loot=[cristal],
        )
        forteresse.add_enemy(vorn)



    def _build_world_2(self):
        """
        Construit les zones principales du CHAPITRE II : Velyra IX.
        Version épurée : pas de velrya_stage, uniquement des flags explicites.
        """
        # --- ROOMS ---
        base = Room(
            "Base rebelle de Velyra",
            "Un bunker dissimulé sous les ruines d’un ancien quartier industriel. "
            "Des écrans grésillent, montrant les patrouilles de drones du Gouverneur Karn."
        )
        quartier = Room(
            "Quartier civil",
            "Des immeubles serrés, des néons blafards, des habitants qui marchent tête baissée "
            "sous l’œil constant des caméras."
        )
        entrepots = Room(
            "Entrepôts civils",
            "De grands hangars où sont stockées les réserves d’énergie et de nourriture. "
            "Des gardes mécaniques veillent sans relâche."
        )
        prison = Room(
            "Prison centrale",
            "Une forteresse de métal noir, hérissée de tourelles automatiques. "
            "C’est ici que sont enfermés Narek et les chefs rebelles."
        )
        citadelle = Room(
            "Citadelle de Karn",
            "Un gratte-ciel blindé entouré de drones, cœur du pouvoir du Gouverneur Karn. "
            "Les IA marchandes y supervisent chaque transaction, chaque mouvement."
        )

        # Connexions linéaires
        base.connect(quartier, "E")
        quartier.connect(entrepots, "E")
        entrepots.connect(prison, "E")
        prison.connect(citadelle, "E")
        
        # Assignation du game aux rooms
        for r in (base, quartier, entrepots, prison, citadelle):
            r.game = self
        
    
        
        # items obtentus dans le chapitre 2
        nanomed = Item(
            "Dose de Nanomédecine",
            "Un cylindre métallique rempli de nanorobots médicaux capables de réparer les tissus "
            "en quelques secondes. Une seule dose. Une seule chance.",
            effect_type="quest",
            value=0,
            usable=False,
            weight=1
        )
        
        # Descriptions alternatives
        entrepots.alt_description_robbery = (
            "Les hangars portent encore les marques de votre raid : portes éventrées, "
            "caisses brisées, drones calcinés. Les civils vous évitent du regard, le "
            "silence oppressant rappelant le prix de vos ressources."
        )
        entrepots.alt_description_corruption = (
            "Les entrepôts sont étrangement silencieux. Plusieurs caisses portent le sceau "
            "du général Akros. Les drones de sécurité vous observent mais ne réagissent pas : "
            "le protocole prioritaire que vous avez acheté les empêche d'intervenir."
        )
        prison.alt_description_after_raid = (
            "La prison porte encore les cicatrices de votre assaut : murs éventrés, tourelles brisées, "
            "cellules ouvertes à la hâte. L’air pue la fumée et la poussière."
        )
        prison.alt_description_after_missiles = (
            "Les murs sont calcinés par les frappes orbitales. Des pans entiers se sont effondrés, "
            "laissant la structure instable. Les systèmes électroniques grésillent encore."
        )
     

        
        

        # --- PNJ : YARA ---
        yara = Character(
            "Yara",
            "Cheffe rebelle d’Eridani, désormais en mission sur Velyra IX. "
            "Son visage porte déjà les cicatrices de la guerre."
        )

        def talk_yara_velyra(player, game, self_char):
            """
            Version propre du système narratif.
            4 états narratifs :
                - intro non faite
                - prison non libérée
                - prison libérée mais Karn vivant
                - Karn mort
            """

            # ----------------------------
            # ÉTAPE 0 : INTRO NON FAITE
            # ----------------------------
            if not getattr(player, "velyra_intro_done", False):
                player.velyra_intro_done = True

                print(
                    "Yara : « Velyra IX est pire qu’Eridani. "
                    "Karn gouverne avec des IA marchandes et des drones. "
                    "Chaque jour, des prisonniers sont exécutés. Parmi eux, mon frère : Narek. »\n"
                )
                print("Elle te fixe :\n"
                    "On a deux options :\n"
                    "  1️⃣ Étudier la planète (DEF ++, Moral --)\n"
                    "  2️⃣ Attaquer immédiatement (ATK ++, pertes sévères)\n")

                choix = ""
                while choix not in ("1", "2"):
                    choix = input("> ").strip()

                if choix == "1":
                    player.defense += 2
                    player.moral -= 1
                    player.reputation += 2
                    player.velyra_study_first = True
                    return (
                        "Vous observez les patrouilles, les schémas de drones, les routes d’approvisionnement.\n"
                        "Chaque nuit, pourtant, Yara reçoit des rapports d’exécutions.\n"
                        "➡️ DEF +2, Moral -1, Réputation +2."
                    )
                else:
                    dmg = player.take_damage(15)
                    player.defense = max(0, player.defense - 1)
                    player.resources = max(0, player.resources - 1)
                    player.atk += 2
                    player.moral += 1
                    player.reputation += 2
                    player.velyra_attack_first = True
                    return (
                        "Le Vigilant plonge dans l’atmosphère et subit un bombardement brutal.\n"
                        f"➡️ PV -{dmg}, DEF -1, Ressources -1, ATK +2, Moral +1, Réputation +2."
                    )

            # ----------------------------
            # ÉTAPE 1 : PRISON NON LIBÉRÉE
            # ----------------------------
            if not getattr(player, "velyra_prison_liberated", False):
                print(
                    "Yara : « On a localisé la prison centrale. Narek est là-bas.\n"
                    "Mais il nous reste presque rien. »\n"
                )
                print(
                    "Deux options :\n"
                    "  1️⃣ Piller les entrepôts civils (Ressources ++, Moral ↓↓↓, Réputation ↓↓↓)\n"
                    "  2️⃣ Corrompre un général de Karn en échange d'item (risqué, missiles possibles)\n"
                )

                choix = ""
                while choix not in ("1", "2"):
                    choix = input("> ").strip()

                # --- Option 1 : PILLER LES CIVILS ---
                if choix == "1":
                    player.velyra_robbed_civilians = True
                    player.resources += 4
                    player.atk += 1
                    player.moral -= 3
                    player.reputation -= 4
                    player.velyra_prison_liberated = True
                    player.narek_alive = True

                    return (
                        "Vous lancez un raid brutal sur les entrepôts civils.\n"
                        "Les hangars débordent d’armes légères, de batteries d’énergie et de caisses de munitions.\n\n"
                        "Les familles courent se mettre à l’abri sous les tirs, des enfants hurlent, "
                        "et les gardes mécaniques tombent un à un.\n"
                        "Dans la panique, vos rebelles arrachent tout ce qu’ils peuvent charger : "
                        "explosifs, blindages portatifs, chargeurs plasma.\n\n"
                        "Avec cet arsenal improvisé, vous frappez directement la prison centrale.\n"
                        "Les murs éclatent sous les charges volées, les tourelles se taisent, "
                        "et les cellules explosent les unes après les autres.\n\n"
                        "Narek surgit dans les décombres, encore enchaîné, mais vivant.\n"
                        "Vous l’avez libéré… au prix de la confiance de tout un peuple.\n\n"
                        "➡️ Ressources +4  |  ATK +1  |  Moral -3  |  Réputation -4."
                    )

                # --- Option 2 : CORRUPTION ---
                import random
                player.velyra_corrupted_general = True

                rare = player.find_item("Module d'énergie stabilisé") or player.find_item("Cristal de propulsion")
                rare_name = rare.name if rare else None
                if rare:
                    player.remove_item(rare)
                    chance_bonus = 0.15
                else:
                    chance_bonus = 0.0
                    print(
                        "Vous n'avez pas d'objet rare à offrir au général.\n"
                        "La corruption sera plus difficile...\n"
                    )

                base_chance = 0.4 + chance_bonus + max(0, player.reputation) * 0.03
                base_chance = min(base_chance, 0.85)
                roll = random.random()

                if roll <= base_chance:
                    # corruption réussie
                    player.velyra_missiles_obtained = True
                    player.resources += 2
                    player.atk += 1
                    player.defense += 1
                    player.moral += 1
                    player.reputation += 2
                    player.velyra_prison_liberated = True
                    player.narek_alive = True

                    texte = (
                        "Le général accepte votre offre.\n"
                        "Grâce aux missiles orbitaux, vous détruisez la prison et libérez Narek.\n"
                        "➡️ ATK +1, DEF +1, Moral +1, Réputation +2."
                    )
                    if rare_name:
                        texte = (
                        f"Vous offrez {rare_name} au général en échange de son aide.\n"
                        + texte
                        )
                    return texte

                else:
                    # corruption ratée
                    dmg = player.take_damage(10)
                    player.defense = max(0, player.defense - 1)
                    player.resources = max(0, player.resources - 1)
                    player.moral -= 1
                    player.reputation -= 1
                    player.velyra_missiles_obtained = True
                    player.velyra_prison_liberated = True
                    player.narek_alive = True

                    return (
                        "La corruption échoue : embuscade.\n"
                        f"➡️ PV -{dmg}, DEF -1, Ressources -1, Moral -1.\n"
                        "Vous capturez malgré tout le terminal des missiles et libérez Narek."
                    )

            # ----------------------------
            # ÉTAPE 2 : PRISON LIBÉRÉE, KARN VIVANT
            # ----------------------------
            if not getattr(player, "velyra_karn_defeated", False):
                if getattr(player, "velyra_missiles_obtained", False):
                    return (
                        "Yara : « Avec les missiles, on va pulvériser la Citadelle de Karn. »\n"
                        "➡️ Rendez-vous à la citadelle."
                    )
                else:
                    return (
                        "Yara : « On infiltrera la citadelle par les conduits de maintenance. »\n"
                        "➡️ Rendez-vous à la citadelle."
                    )

            # ----------------------------
            # ÉTAPE 3 : KARN MORT
            # ----------------------------
            return (
                "Yara : « Velyra est libre. Grâce à toi. »\n"
                "Narek : « Et ce n’est que le début. »"
            )

        yara.on_talk = talk_yara_velyra
        base.add_character(yara)

        # --- PNJ : Nommera, survivante civile ---
        nommera = Character(
            "Nommera",
            "Une jeune femme aux mains couvertes de poussière, le regard creux mais lucide."
        )

        def talk_nommera(player, game, self_char):

            # Cas 1 : PILLAGE des civils (route très négative)
            if getattr(player, "velyra_robbed_civilians", False):

                return (
                    "Nommera : C’était vous… Je vous ai vu défoncer les portes des hangars. \n"
                    "Son regard tremble :\n"
                    "Vous avez pris nos vivres… nos armes… et laissé des familles dans la poussière. "
                    "Vous avez sauvé quelqu’un là-bas, je suppose. Mais ici, on pleure encore.\n"
                    "Elle détourne les yeux :\n"
                    "On ne vous dénoncera pas. On n’a plus personne à qui parler, de toute façon."
                )

            # Cas 2 : CORRUPTION — deal secret avec Akros
            if getattr(player, "velyra_corrupted_general", False):

                return (
                    "Nommera : Les drones… ils ne nous surveillent plus. \n"
                    "Elle te fixe longuement, hésitant entre gratitude et malaise.\n"
                    "Vous avez gagné quelque chose… mais vous avez dû payer quelqu’un pour ça. "
                    "Le général Akros ne fait rien gratuitement. \n"
                    "Elle croise les bras :\n"
                    "Je ne sais pas ce que vous lui avez donné… mais ça retombe toujours sur quelqu’un. Toujours."
                )

            # Cas théorique : aucun choix encore (ne devrait jamais arriver)
            return (
                "Nommera : Les entrepôts sont dangereux… faites attention."
            )
      
        nommera.on_talk = talk_nommera
        entrepots.add_character(nommera)
        
        # --- PNJ : NAREK, frère de Yara ---
        narek = Character(
            "Narek",
            "Un jeune rebelle amaigri mais déterminé, encore marqué par son emprisonnement."
        )
        def talk_narek(player, game, self_char):
            """ Dialogue variant selon la route choisie pour le libérer."""
            
            # Route 1 : PILLAGE
            if getattr(player, "velyra_robbed_civilians", False):
                return (
                    "Narek : Je t’en dois une… mais je sais ce que tu as fait.\n"
                    "Il détourne le regard.\n"
                    "Des familles ont souffert pour me sortir d’ici. Je vis grâce à elles."
                )

            # Route 2 : MISSILES
            if getattr(player, "velyra_missiles_obtained", False):
                return (
                    "Narek : Tu as frappé juste. Les missiles… je ne les oublierai jamais.\n"
                    "On a perdu quelques camarades dans l’explosion, mais tu m'as sauvé."
                )

            # Route neutre (ne devrait pas arriver)
            return "Narek : « Merci de m'avoir sorti de là. »"
        narek.on_talk = talk_narek
        prison.add_character(narek)

        # Ennemis


        prison.add_enemy(Enemy("Drone Sentinel", hp=70, atk=10, defense=6,is_boss=False, loot=[nanomed])) 
        citadelle.add_enemy(Enemy("Gouverneur Karn", hp=160, atk=16, defense=10, is_boss=True))

        self.rooms_world2 = {
            "Base rebelle de Velyra": base,
            "Quartier civil": quartier,
            "Entrepôts civils": entrepots,
            "Prison centrale": prison,
            "Citadelle de Karn": citadelle,
        }



    def _build_world_3(self):
        """
        Construit le CHAPITRE III — Aurelion Prime.
        Version validée : infiltration OU révélation → passage par Le Nœud
        avec choix illusions/briser → combat final ou fin sombre.
        """

        # =============== ROOMS ===============
        district = Room(
            "District d’Or",
            "Un quartier luxueux où tout semble parfait : rues propres, jardins calibrés, "
            "habitants souriants… mais dont les yeux semblent vides."
        )
        
        holo = Room(
            "Quartier des Hologrammes",
            "Des illusions mouvantes envahissent les rues : visages qui se dédoublent, "
            "publicités vivantes, faux souvenirs, et ombres qui n'appartiennent à personne."
        )

        node = Room(
            "Le Nœud",
            "Un complexe gigantesque regroupant les serveurs neuronaux d’Aurelion Prime. "
            "Il régule émotions, souvenirs et réactions de toute la population."
        )

        palace = Room(
            "Palais de Lumière",
            "Un ensemble de jardins flottants, ponts de cristal et escaliers étincelants. "
            "Les serviteurs semblent humains… mais agissent comme des programmes."
        )

        throne = Room(
            "Salle du Trône",
            "Une vaste pièce circulaire baignée d’or, où Seren Taal attend, immobile, "
            "dans un halo d’illusions."
        )

        # =============== CONNECTIONS ===============
        district.connect(holo, "E")
        holo.connect(node, "E")
        node.connect(palace, "E")
        palace.connect(throne, "E")

        # Assignation du game aux rooms
        for r in (district, holo, node, palace, throne):
            r.game = self

        # =============== ALT DESCRIPTIONS ===============
        district.alt_description_infiltrate = (
            "Vous passez pour des habitants d’élite. Les regards sont admiratifs… mais vides."
        )
        district.alt_description_reveal = (
            "Des drones vous surveillent. Les habitants gardent leurs distances, méfiants."
        )

        node.alt_description_break = (
            "Les illusions se fissurent. Les habitants errent, effondrés, découvrant "
            "les horreurs qu’ils ignoraient. Cris, larmes, terreur."
        )
        node.alt_description_keep = (
            "Les illusions brillent comme jamais : bonheur forcé, sourires figés, "
            "éclats de rire synthétiques."
        )

        # =============== PNJ ===============
        citizen = Character(
            "Citoyen doré",
            "Un habitant riche dont les émotions sont filtrées par les serveurs du Nœud."
        )

        def talk_citizen(player, game, self_char):
            if player.ap_choice_infiltrate:
                return "Citoyen doré : « Vous êtes splendides. Vous avez le rang pour être ici. »"
            if player.ap_choice_reveal:
                return "Citoyen doré : « Vous êtes un intrus dangereux. Ne touchez à rien. »"
            return "Citoyen doré : « Aurelion est parfait. Les autres mondes souffrent ? Ils sont faibles. »"

        citizen.on_talk = talk_citizen
        district.add_character(citizen)

        glitch = Character(
            "Habitant glitché",
            "Son corps scintille comme un hologramme mal calibré. Sa voix tremble, en écho."
        )

        def talk_glitch(player, game, self_char):
            if not getattr(player, "aurelion_surprise_done", False):
                return "…v…v…vvous… n’êtes pas… attendus…"
            return "Les murs… regardent… attention à… Seren… Taa— *signal perdu*."

        glitch.on_talk = talk_glitch
        holo.add_character(glitch)


        # =============== ENNEMIS ===============
        palace.add_enemy(Enemy("Gardien Blanc", hp=90, atk=22, defense=8))
        taal = Enemy(
            "Seren Taal",
            hp=240,
            atk=30,
            defense=12,
            is_boss=True,
            loot=[]
        )
        throne.add_enemy(taal)

        # =============== STOCKAGE ===============
        self.rooms_world3 = {
            "District d’Or": district,
            "Quartier des Hologrammes": holo,
            "Le Nœud": node,
            "Palais de Lumière": palace,
            "Salle du Trône": throne,
        }



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
    #   Transition vers le Monde 2 — Velyra IX
    # =========================================================
    def transition_to_world_2(self):
            """
            Départ d’Eridani Prime et arrivée sur Velyra IX.
            Appelée après la défaite de Vorn.
            """
            
            if self.player.world2_started:
                return  # Empêche de relancer 50 fois

            self.player.world2_started = True

            self.player.log("Le Vigilant a quitté Eridani Prime en direction de Velyra IX.")

            print("\n🚀 Le Vigilant s’élève au-dessus d’Eridani Prime.")
            print("Les mineurs et les rebelles acclament votre nom alors que le vaisseau perce les nuages.")
            print("Quelques jours plus tard, les capteurs détectent Velyra IX : une planète-machine sous la tyrannie de Karn.\n")

            # Construction du monde 2
            self._build_world_2()
            start_room = self.rooms_world2["Base rebelle de Velyra"]
            self.player.current_room = start_room

            print("🌌 CHAPITRE II — VELYRA IX 🌌\n")
            print(start_room.get_long_description())
            print("\n" + self.help_text() + "\n")

            # ⚠ On force immédiatement les deux grands choix avec Yara
            yara = start_room.find_character("Yara")
            if yara and yara.on_talk:
                print("\nYara s’avance vers vous dès votre arrivée.\n")

                # 1) Étudier / Attaquer
                texte = yara.on_talk(self.player, self, yara)
                if texte:
                    print(texte + "\n")

                # 2) Voler les civils / Corrompre le général
                texte2 = yara.on_talk(self.player, self, yara)
                if texte2:
                    print(texte2 + "\n")

            print("Demandez à Yara le plan pour la suite. \nVous pouvez ensuite explorer Velyra IX. Utilisez 'g E' pour rejoindre le Quartier civil.\n")


    # =========================================================
    #   ATTACK SURPRISE — Quartier civil, Monde 2
    # =========================================================
    def _attack_surprise_velyra(self):
        """
        Embuscade dans le Quartier civil : 
        3 ennemis attaquent l’un après l’autre via le vrai système de combat.
        """
        print("\n⚠️ EMBUSCADE ! Des drones surgissent des toits et ouvrent le feu !\n")

        # Les ennemis se battent dans CET ordre
        enemies = [
            Enemy("Drone éclaireur", hp=35, atk=7, defense=2),
            Enemy("Drone éclaireur", hp=35, atk=7, defense=2),
            Enemy("Drone de patrouille", hp=55, atk=10, defense=3),
        ]

        for e in enemies:
            print(f"Un {e.name} vous attaque !\n")
            
            # On place l’ennemi dans la room actuelle pour le système normal
            self.player.current_room.enemies.append(e)

            # Combat obligatoire
            output = actions.attack(self, e.name)
            print(output)

            # Le combat continue tant que l’ennemi n’est pas mort
            while e.is_alive() and self.player.is_alive():
                output = actions.attack(self, e.name)
                print(output)

            # Nettoyage : enlever l’ennemi
            self.player.current_room.enemies.remove(e)

            if not self.player.is_alive():
                print("Vous êtes mort. Game Over.")
                self.running = False
                return

        print("\nVous survivez à l'embuscade !")
        print("➡️ Ressources +1 | Réputation +1\n")
        self.player.resources += 1
        self.player.reputation += 1


    # =========================================================
    #   ATTACK SURPRISE — Quartier des Hologrammes, Monde 3
    # =========================================================
    def _attack_surprise_aurelion(self):
        """
        Attaque surprise dans le Quartier des Hologrammes.
        Les illusions 'glitchent', deux vagues d'ennemis holographiques attaquent.
        """
        print("\n⚠️ Les hologrammes se déchirent autour de vous…")
        print("Des visages se dédoublent, des passants se figent, puis explosent en lumière.")
        print("Une voix froide murmure : « Anomalie cognitive détectée. Neutralisation. »\n")

        # Ennemis (vague 1)
        enemies_wave1 = [
            Enemy("Spectre Holographique", hp=45, atk=12 + (2 if self.player.ap_choice_reveal else 0), defense=3),
            Enemy("Spectre Holographique", hp=45, atk=12 + (2 if self.player.ap_choice_reveal else 0), defense=3),
        ]

        # Ennemis (vague 2)
        enemies_wave2 = [
            Enemy("Garde Éclaté", hp=60, atk=16 + (3 if self.player.ap_choice_reveal else 0), defense=4),
        ]

        all_waves = [enemies_wave1, enemies_wave2]

        for wave in all_waves:
            for enemy in wave:
                print(f"Un {enemy.name} surgit de la lumière fracturée !\n")
                self.player.current_room.enemies.append(enemy)

                output = actions.attack(self, enemy.name)
                print(output)

                while enemy.is_alive() and self.player.is_alive():
                    output = actions.attack(self, enemy.name)
                    print(output)

                self.player.current_room.enemies.remove(enemy)

                if not self.player.is_alive():
                    print("Vous êtes mort. Game Over.")
                    self.running = False
                    return

        print("\n✨ Les illusions se referment lentement… mais quelque chose a changé.")
        print("➡️ Moral +1 | Réputation +1\n")

        self.player.moral += 1
        self.player.reputation += 1


    # =========================================================
    #   FIN DU MONDE 2 — Choix final
    # =========================================================
    def end_world_2(self):
        """
        Épilogue du Chapitre II après la mort de Karn.
        Gère la présence ou non de la nanomédecine et le choix final :
            - sauver Yara
            - sauver Narek
            - ou aucun si l'item n'existe pas.
        """

        print("\nLa Citadelle s'effondre dans un rugissement métallique.")
        print("Les IA se taisent une à une… Velyra IX respire enfin.\n")

        player = self.player

        # Vérifier présence nanomédecine
        nano = player.find_item("Dose de Nanomédecine")

        print("Dans les décombres… deux silhouettes immobiles.")
        print("Yara, ta commandante rebelle… Et Narek, son frère.\n")
        print("Ils sont tous les deux grièvement blessés. Ils ne survivront pas longtemps.\n")

        # -------------------------------------------------------------------------
        # CAS 1 — PAS DE NANOMÉDECINE : aucun ne peut survivre.
        # -------------------------------------------------------------------------
        if not nano:
            print("❌ Vous fouillez rapidement votre inventaire…")
            print("Mais il ne reste PLUS aucune dose de nanomédecine.\n")
            print("Yara et Narek vous regardent faiblement…")
            print("Leurs mains se serrent. Ils meurent ensemble, en héros silencieux.\n")

            # Conséquences sans choix
            player.moral -= 2
            player.reputation += 3

            print("➡️ Moral -2 | Réputation +3\n")
            print("Les rebelles vous regardent avec gravité, mais sans colère :")
            print("« Tu n’avais pas le choix… »\n")

            self._end_velyra_cinematic()
            self.player.aurelion_ready = True
            return

        # -------------------------------------------------------------------------
        # CAS 2 — NANOMÉDECINE DISPONIBLE : choix final.
        # -------------------------------------------------------------------------

        print("Vous n’avez qu’une seule dose de nanomédecine.")
        print("Un seul survivra.\n")
        print("Qui sauvez-vous ?\n")
        print("1️⃣ YARA — La rebelle cheffe et stratège")
        print("2️⃣ NAREK — Son frère, le symbole de l’espoir populaire\n")

        choix = ""
        while choix not in ("1", "2"):
            choix = input("> ").strip()

        # Utilisation de l’item (retiré de l’inventaire)
        player.remove_item(nano)

        # --- Sauver YARA ---
        if choix == "1":
            print("\n💉 Vous injectez la dose à Yara.")
            print("Elle respire à nouveau… mais ses yeux s’emplissent de larmes.")
            print("Narek murmure : « Je t’aime… Sois forte. » avant de s’éteindre.\n")

            # Stats
            player.moral += 1
            player.reputation += 1
            player.atk += 1

            print("➡️ Moral +1 | Réputation +1 | ATK +1\n")
            print("Yara jure de continuer le combat à ses côtés.\n")

        # --- Sauver NAREK ---
        else:
            print("\n💉 Vous injectez la dose à Narek.")
            print("Il ouvre les yeux… juste le temps de voir sa sœur mourir.")
            print("Elle murmure : « Continue… pour nous. » avant de s'éteindre.\n")

            # Stats
            player.moral -= 1
            player.reputation += 2
            player.defense += 1

            print("➡️ Moral -1 | Réputation +2 | DEF +1\n")
            print("Narek jure de porter la flamme de la rébellion.\n")
        self._end_velyra_cinematic()
        self.player.aurelion_ready = True

    # =========================================================
    #   CINÉMATIQUE DE FIN DE VELYRA IX
    # =========================================================
    def _end_velyra_cinematic(self):
        """ Cinematic de fin de Velyra IX, après le choix final. """
        print("\nFIN DE LA LIBÉRATION DE VELYRA IX\n")
        print("Les rebelles t’entourent. Certains pleurent, d’autres crient victoire.")
        print("Les citoyens émergent des ruines, voyant pour la première fois un ciel sans drones.\n")

        print("La bannière de la liberté est hissée au sommet de la Citadelle brisée.")
        print("Des milliers d’écrans projettent ton nom : le libérateur de Velyra.\n")

        print("Le Vigilant décolle lentement, traversant les nuages rosés…")
        print("Un nouveau monde t’attend.\n")

        print("🌌 Planète Velyra IX — LIBÉRÉE 🌌\n")
        print("➡️ Utiliser la touche entrée pour voyager vers Aurelion Prime\n")

    # =========================================================
    #   TRANSITION VERS LE MONDE 3 — AURELION PRIME
    # =========================================================
    def transition_to_world_3(self):
        """
        Transition complète vers le CHAPITRE III — Aurelion Prime.
        Déclenchée après la fin du monde 2.
        """

        if getattr(self.player, "world3_started", False):
            return

        self.player.world3_started = True
        self.player.log("Le Vigilant approche d’Aurelion Prime.")

        print("\n🚀 Le Vigilant approche d’une planète d’or et de lumière.")
        print("Depuis l’espace, Aurelion Prime ressemble à un joyau taillé.")
        print("Cités parfaites, océans turquoise, lignes géométriques irréprochables.\n")

        print("L’atterrissage se déroule dans un calme étrange.")
        print("Tout semble idyllique… trop idyllique.\n")

        print("Les habitants sourient, mais leurs yeux sont froids.")

        # Construction du monde
        self._build_world_3()

        # Placement du joueur
        start_room = self.rooms_world3["District d’Or"]
        self.player.current_room = start_room

        print("🌌 CHAPITRE III — AURELION PRIME 🌌\n")
        print(start_room.get_long_description())
        print("\n" + self.help_text() + "\n")

        print("Un drone de sécurité vous scanne brutalement.\n")
        print("CHOIX IMMÉDIAT :\n")
        print("1️⃣ S’infiltrer (DEF ↑, Réputation ↑, Moral ↓)")
        print("2️⃣ Révéler la vérité (HP ↓, ATK ↑, Réputation ↓, Moral ↑)\n")


        choix = ""
        while choix not in ("1", "2"):
            choix = input("> ").strip()

        # INFILTRATION
        if choix == "1":
            self.player.ap_choice_infiltrate = True
            self.player.defense += 1
            self.player.reputation += 2
            self.player.moral -= 1

            print("\nVous adoptez des identités locales et pénétrez la haute société.")
            print("➡️ DEF +1 | Réputation +2 | Moral -1\n")

        # RÉVÉLATION
        else:
            self.player.ap_choice_reveal = True
            dmg = self.player.take_damage(15)
            self.player.atk += 1
            self.player.reputation -= 2
            self.player.moral += 1

            print("\nVous montrez la vérité devant une foule… qui éclate de rire.")
            print(f"Les gardes interviennent : PV -{dmg}")
            print("➡️ ATK +1 | Réputation -2 | Moral +1\n")

        print("Explorez maintenant Aurelion Prime.")
        print("Tapez t citoyen doré pour parler à un habitant.")
        print("Utilisez 'g E' pour rejoindre le Quartier des Hologrammes.\n")


    # =========================================================
    #   FIN DU MONDE 3 — Choix final après Seren Taal
    # =========================================================
    def end_world_3(self):
        """
        Fin du Chapitre III — choix moral final après le face-à-face
        contre Seren Taal.
        """

        print("\n🏛️ Vous entrez dans la Salle du Trône… Seren Taal vous attend.\n")

        # Si la fin sombre est déjà choisie
        if getattr(self.player, "ap_taal_alliance", False):
            print("Vous régnez désormais à ses côtés sur un empire parfait… et oppressif.")
            print("FIN SOMBRE — TYRANNIE ABSOLUE.\n")
            self.running = False
            return

        # Si Seren Taal vient d’être tuée (combat)
        if getattr(self.player, "ap_taal_dead", False):
            print("\n⚔️ Seren Taal tombe à genoux. Les illusions s’effondrent.")
            print("Les habitants retrouvent leurs vraies émotions.")
            print("Les rebelles des mondes 1 et 2 se rassemblent.\n")

            ally = "Yara" if getattr(self.player, "yara_alive", True) else "Narek"
            print(f"{ally} : « Tu as libéré trois mondes. Le Système Epsilon te doit tout. »\n")

            print("🌅 FIN HEUREUSE — LA LIBERTÉ RENAÎT\n")
            self.running = False
            return

        # Sinon : choix d’alliance AVANT le combat
        print("Seren Taal te tend la main :")
        print("« Rejoins-moi. Partage mon trône. Gouverne un empire parfait. »\n")

        print("1️⃣ Accepter (Fin sombre immédiate)")
        print("2️⃣ Refuser (lance le combat final)\n")

        choix = ""
        while choix not in ("1", "2"):
            choix = input("> ").strip()

        if choix == "1":
            self.player.ap_taal_alliance = True
            self.player.moral -= 5
            self.player.reputation -= 5
            print("\n🌑 Vous prenez sa main.")
            print("Vous devenez les souverains d’un empire brillant… et totalitaire.")
            print("FIN SOMBRE.\n")
            self.running = False
            return

        print("\n🔥 Vous refusez. Seren Taal active son exo-armure.")
        print("« Alors meurs comme les faibles. »")
        print("➡️ Utilisez : a Seren Taal\n")

    # =========================================================
    #   HELP TEXT — Commandes disponibles
    # =========================================================
    def help_text(self):
        """Retourne la liste des commandes disponibles pour affichage permanent."""
        return (
            "Commandes disponibles :\n"
            "g : aller <direction> | retour | o : observer | p : prendre <objet> | j : jeter <objet> | i : inventaire | e : examiner <objet> |\n"
            "t : parler <nom> | a : attaquer <ennemi> | u : utiliser <objet> | s : statut | h : historique | x : analyser <nom> | ia | q : quitter"
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
                
                
            # --- Attaque surprise Quartier civil (monde 2) ---
            room = self.player.current_room
            if (room.name == "Quartier civil" and not getattr(self.player, "velyra_surprise_done", False)):
                self.player.velyra_surprise_done = True
                self._attack_surprise_velyra()


            # Si Vorn vient d'être tué : transition à la FIN du tour car sinon il manque "vorn fait tomber cristal..."
            if getattr(self.player, "vorn_defeated", False):
                self.player.vorn_defeated = False
                self.transition_to_world_2()
                continue
            
            
            # Si Karn vient d'être tué : transition à la FIN du tour car sinon il manque "karn s'effondre..."
            if getattr(self.player, "velyra_karn_defeated", False):
                self.player.velyra_karn_defeated = False
                self.end_world_2()
                continue
            
            
            # Transition vers Monde 3 (après fin monde 2)
            if getattr(self.player, "aurelion_ready", False):
                self.player.aurelion_ready = False
                self.transition_to_world_3()
                continue
            
            # === Si les Gardiens Blancs viennent d'être tués ===
            if room.name == "Palais de Lumière":
                # Check if no White Guardians remain
                remaining = any(e.name == "Gardien Blanc" and e.is_alive() for e in room.enemies)
                if not remaining and not getattr(self.player, "ap_guardians_cleared", False):
                    self.player.ap_guardians_cleared = True
                    print("\n⚔️ Les deux Gardiens Blancs s'effondrent dans un fracas métallique.")
                    print("Les portes en or massif vibrent… puis s’ouvrent lentement vers la Salle du Trône.")
                    print("Une voix éthérée murmure : « Approche, élève… »\n")


            # --- Attaque surprise Quartier des Hologrammes (monde 3) ---
            if (room.name == "Quartier des Hologrammes"
                and getattr(self.player, "world3_started", False)
                and not getattr(self.player, "aurelion_surprise_done", False)):
                
                self.player.aurelion_surprise_done = True
                self._attack_surprise_aurelion()

            # === Réactions post-Nœud (Monde 3) ===
            if room.name in ("District d’Or", "Quartier des Hologrammes") and getattr(self.player, "ap_cleared_node", False):

                if self.player.ap_break_illusions:
                    print("\n🌪️ Les illusions sont brisées :")
                    if room.name == "District d’Or":
                        print("Les habitants paniquent, certains pleurent en découvrant la vérité.")
                    else:
                        print("Les hologrammes scintillent, instables… certains s’effondrent comme du verre.")
                else:
                    print("\n✨ Les illusions continuent d’opérer. Tout semble parfait… trop parfait.")

            # === Déclencheur automatique du monologue de Seren Taal ===
            if room.name == "Salle du Trône" and not getattr(self.player, "ap_taal_confronted", False):

                self.player.ap_taal_confronted = True
                print("\n👑 Seren Taal se lève de son trône, un sourire calme au visage.\n")
                print("« Te voilà enfin… Capitaine. »\n")
                print("« J’ai bâti un monde parfait. Sans douleur. Sans guerre. »")
                print("« Rejoins-moi. Gouvernons ensemble. »\n")

                print("1️⃣ Accepter l’alliance (fin sombre)")
                print("2️⃣ Refuser (déclenche le combat final)\n")

                choix = ""
                while choix not in ("1", "2"):
                    choix = input("> ").strip()

                if choix == "1":
                    self.player.ap_taal_alliance = True
                    self.player.moral -= 5
                    self.player.reputation -= 5
                    self.player.atk += 2
                    self.player.defense += 1

                    print("\n🌑 Vous prenez sa main. Vous devenez co-dirigeant d’un empire parfait… et oppressif.")
                    print("FIN SOMBRE.\n")
                    self.running = False
                    return

                # Refus → combat
                print("\n🔥 Vous refusez.")
                print("Seren Taal active son exo-armure : « Alors tu mourras comme les autres. »\n")
                print("➡️ Utilisez : a Seren Taal\n")

            
            # Si Seren Taal vient d'être tuée, lancer fin du monde 3
            if getattr(self.player, "ap_taal_dead", False):
                self.player.ap_taal_dead = False
                self.end_world_3()
                continue



            # Affiche toujours les commandes après chaque action
            print("\n" + self.help_text() + "\n")


# Point d’entrée du programme
if __name__ == "__main__":
    g = Game()
    g.play()
