# game.py
"""
Module principal : gestion du jeu, de la map et de la boucle principale.

Classes
-------
Game
"""

from room import Room
from player import Player
from item import Item
from character import Character
from enemy import Enemy
from command import Command

DEBUG = False  # mettre à True pour voir d'éventuels messages de debug


class Game:
    """Classe principale gérant le monde, le joueur et la boucle de jeu."""

    def __init__(self):
        # Création des lieux
        self._create_world()

        # Demander le nom du joueur
        name = input("Entrez le nom de votre capitaine : ").strip()
        if not name:
            name = "Capitaine sans nom"

        # Création du joueur à la baie de crash
        self.player = Player(name, self.baie)

        # Flag de boucle principale
        self.running = True

    # ------------------------------------------------------------------
    # Construction du monde
    # ------------------------------------------------------------------

    def _create_world(self):
        """Crée les salles, les objets, les PNJ, les ennemis et les liens."""

        # --- Salles principales ---
        self.baie = Room(
            "Baie de crash",
            "dans la baie de crash du Vigilant, entouré de débris fumants."
        )
        self.plaines = Room(
            "Plaines d'Eridani",
            "sur les plaines froides d'Eridani, balayées par un vent chargé de poussière."
        )
        self.grotte = Room(
            "Grotte cristalline",
            "dans une grotte éclairée par des cristaux instables."
        )
        self.bunker = Room(
            "Bunker de maintenance",
            "dans un ancien bunker technique enfoui sous la roche."
        )
        self.ville = Room(
            "Ville minière",
            "au cœur d'une ville minière misérable, saturée de propagande."
        )
        self.marche = Room(
            "Marché clandestin",
            "au milieu d'un marché clandestin bruyant et surpeuplé."
        )
        self.tour = Room(
            "Tour de contrôle",
            "dans la tour de contrôle, dominant les installations d'Eridani."
        )
        self.plateforme = Room(
            "Plateforme orbitale",
            "sur une plateforme orbitale à ciel ouvert, dominant la planète."
        )

        # --- Liens (N, S, E, W, U, D) ---
        # Baie <-> Plaines
        self.baie.exits["N"] = self.plaines
        self.plaines.exits["S"] = self.baie

        # Plaines <-> Grotte
        self.plaines.exits["E"] = self.grotte
        self.grotte.exits["W"] = self.plaines

        # Grotte <-> Bunker
        self.grotte.exits["S"] = self.bunker
        self.bunker.exits["N"] = self.grotte

        # Baie <-> Ville
        self.baie.exits["E"] = self.ville
        self.ville.exits["W"] = self.baie

        # Ville -> Marché (sens unique vers le bas)
        self.ville.exits["D"] = self.marche
        # Marché -> Bunker (on remonte par des tunnels)
        self.marche.exits["N"] = self.bunker

        # Baie <-> Tour (vertical U/D)
        self.baie.exits["U"] = self.tour
        self.tour.exits["D"] = self.baie

        # Tour <-> Plateforme
        self.tour.exits["E"] = self.plateforme
        self.plateforme.exits["W"] = self.tour

        # --- Objets ---
        # Baie : petits débris
        balise = Item(
            "balise de détresse",
            "une petite balise de détresse du Vigilant.",
            2
        )
        self.baie.inventory.append(balise)

        # Grotte : fragment de noyau
        fragment = Item(
            "fragment de noyau",
            "un fragment de noyau énergétique instable.",
            1
        )
        self.grotte.inventory.append(fragment)

        # Bunker : kit de réparation
        kit = Item(
            "kit de réparation",
            "un kit de réparation standard pour vaisseau.",
            3
        )
        self.bunker.inventory.append(kit)

        # Marché : carte d'Eridani
        carte = Item(
            "carte d'Eridani",
            "une carte grossière des principaux sites d'Eridani Prime.",
            1
        )
        self.marche.inventory.append(carte)

        # Tour : balise quantique
        beamer = Item(
            "balise quantique",
            "un prototype de téléporteur expérimental (encore instable).",
            2
        )
        self.tour.inventory.append(beamer)

        # --- PNJ ---
        # Baie
        tech = Character(
            "Lira",
            "une technicienne du Vigilant, couverte de suie.",
            self.baie,
            [
                "On a perdu beaucoup de modules... Mais tant qu'on trouve un cristal de propulsion, on peut repartir.",
                "J'ai vu une créature dans les plaines, elle semblait se nourrir de cristaux..."
            ]
        )
        self.baie.characters.append(tech)

        # Plaines
        scout = Character(
            "Tedan",
            "un éclaireur local, méfiant mais curieux.",
            self.plaines,
            [
                "Les Raptors des collines adorent les cristaux instables. Si tu en cherches, commence par les chasser.",
                "Les rebelles se cachent près du bunker, à l'Est puis au Sud."
            ]
        )
        self.plaines.characters.append(scout)

        # Grotte
        vieux = Character(
            "Vieil explorateur",
            "un homme ridé, les yeux illuminés par la lumière des cristaux.",
            self.grotte,
            [
                "Les cristaux d'Eridani sont instables. Certains explosent, d'autres alimentent des vaisseaux.",
                "Si tu trouves un cristal de propulsion, ne le laisse pas tomber entre de mauvaises mains."
            ]
        )
        self.grotte.characters.append(vieux)

        # Ville
        marchand_info = Character(
            "Archiviste",
            "un archiviste fatigué, gardien de vieux registres.",
            self.ville,
            [
                "Le capitaine Vorn a ruiné cette planète, mais quelques résistants tiennent encore.",
                "Au marché clandestin, on échange tout... sauf la liberté."
            ]
        )
        self.ville.characters.append(marchand_info)

        # Marché
        courtier = Character(
            "Courtier",
            "un courtier au sourire douteux.",
            self.marche,
            [
                "Quelques rumeurs disent qu'un cristal de propulsion a été vu dans les plaines.",
                "Si tu veux quitter Eridani, tu auras besoin de ce cristal. Et d'un peu de chance."
            ]
        )
        self.marche.characters.append(courtier)

        # Tour
        oracle = Character(
            "Oracle",
            "une IA holographique projetée au centre de la salle de contrôle.",
            self.tour,
            [
                "Trajectoires stables seulement si le module de propulsion est opérationnel.",
                "Les signaux rebelles convergent vers Nova Terra... mais tu dois d'abord sauver ton équipage."
            ]
        )
        self.tour.characters.append(oracle)

        # Plateforme
        rebelle = Character(
            "Caporale Yara",
            "une combattante rebelle, regard déterminé.",
            self.plateforme,
            [
                "Si tu réussis à remettre le Vigilant en marche, ramène ces gens loin d'ici.",
                "On te couvrira depuis la surface. Toi, occupe-toi du vaisseau."
            ]
        )
        self.plateforme.characters.append(rebelle)

        # --- Ennemis ---
        # Raptor dans les plaines, avec le cristal en loot
        cristal = Item(
            "cristal de propulsion",
            "un cristal énergétique indispensable à la réparation du Vigilant.",
            4
        )
        raptor = Enemy(
            "Raptor des collines",
            "une créature féroce recouverte de cristaux luminescents.",
            self.plaines,
            hp=15,
            atk=5,
            loot=cristal
        )
        self.plaines.enemies.append(raptor)

        # Drone de sécurité dans le bunker
        drone = Enemy(
            "Drone de sécurité",
            "un ancien drone de maintenance devenu agressif.",
            self.bunker,
            hp=10,
            atk=4,
            loot=None
        )
        self.bunker.enemies.append(drone)

        # Sentinelle sur la plateforme
        sentinelle = Enemy(
            "Sentinelle orbitale",
            "une sentinelle robotique protégeant l'accès aux systèmes de lancement.",
            self.plateforme,
            hp=18,
            atk=6,
            loot=None
        )
        self.plateforme.enemies.append(sentinelle)

    # ------------------------------------------------------------------
    # Boucle principale
    # ------------------------------------------------------------------

    def welcome(self):
        """Affiche le texte d'introduction du jeu."""
        print(
            "\nEn 2239, le vaisseau interstellaire 'Vigilant' s'est écrasé sur Eridani Prime.\n"
            "Vous devez explorer la planète, rallier des alliés et trouver un cristal\n"
            "de propulsion pour réparer le vaisseau et sauver votre équipage."
        )
        print("\nTapez 'help' pour voir la liste des commandes.\n")
        print(self.player.current_room.get_long_description())

    def play(self):
        """Boucle principale du jeu."""
        self.welcome()

        while self.running:
            try:
                raw = input("> ")
            except (EOFError, KeyboardInterrupt):
                print("\nInterruption. Fin du jeu.")
                break

            cmd = Command(raw)
            output = cmd.execute(self)

            if output:
                print(output)


if __name__ == "__main__":
    game = Game()
    game.play()
