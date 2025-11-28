# 🌌 **THE STELLAR REBELLION — Voyage du *Vigilant***

## 🚀 Présentation générale

**The Stellar Rebellion** est un jeu d’aventure textuel développé en Python dans le cadre du cours TBA (ESIEE Paris).
Le joueur incarne un membre de l’équipage du vaisseau scientifique **Vigilant**, conçu pour offrir à l’humanité une nouvelle planète habitable après la destruction de la Terre.

Une anomalie gravitationnelle interrompt le voyage :
le Vigilant s’écrase sur une planète inconnue, déclenchant une série de choix, de dilemmes moraux et de combats à travers **quatre mondes** du Système Epsilon.

Le but du jeu est de :

* survivre,
* explorer des villes hostiles,
* recruter des alliés,
* gérer ses ressources,
* améliorer le Vigilant,
* et enfin **sauver l’humanité**.

---

# 🧭 Objectifs du jeu

* Explorer 4 mondes : **Eridani Prime → Velyra IX → Aurelion Prime → Nova Terra**
* Prendre des décisions influençant le moral, l’attaque, la défense et les ressources.
* Combattre des ennemis via un système de combat simple mais stratégique.
* Récupérer des objets essentiels (ex : cristal de propulsion).
* Reconstruire le Vigilant et mener la rébellion interplanétaire.

---

# ⚙️ Mécaniques principales

## **Statistiques du joueur**

* **HP** — Santé
* **ATK** — Puissance d’attaque
* **DEF** — Défense
* **MORAL** — Impacte les dialogues et certains embranchements
* **RESSOURCES** — Énergie / matériel utile pour réparer le Vigilant
* **INVENTAIRE** — Objets collectés (avec descriptions)

## **Système de combat**

* Tour par tour
* Dégâts = ATK - DEF adverse (minimum 0)
* Les ennemis peuvent lâcher des objets

## **Interactions**

* PNJ
* Objets à ramasser
* Déplacements entre zones
* Choix narratifs persistants
* IA Quiz (système optionnel)

---

# 🗺️ Les 4 Mondes (Version Résumée & Professionnelle)

## 🌑 **MONDE 1 — ERIDANI PRIME : Oppression et rébellion**

Première planète du jeu, monde minier sous le contrôle du **Capitaine Vorn**.

Points centraux :

* Crash du Vigilant
* Premier dilemme : sauver l’équipage ou les ressources
* Découverte d’un avant-poste minier, d’un marché et d’une cité-forteresse
* Interaction avec **Ralen** et **Yara**, la cheffe rebelle
* Quête du **cristal de propulsion**
* Boss final : **Vorn**

Le joueur répare partiellement le vaisseau et quitte la planète.

---

## 🔧 **MONDE 2 — VELYRA IX : Le Masque du Progrès**

Planète cybernétique dirigée par **Karn**, utilisant IA et drones pour contrôler la population.

Points centraux :

* Attaque immédiate OU infiltration stratégique
* Prison principale où est emprisonné **Narek**, frère de Yara
* Dilemme majeur : voler les civils ou corrompre un général
* Missiles régionaux, IA militaire, documents secrets
* Boss final : **Karn**, en exo-armure

La planète est libérée et le Vigilant obtient une avancée technologique majeure.

---

## 🌀 **MONDE 3 — AURELION PRIME : Le Jardin du Mensonge**

Cité parfaite, luxueuse, mais entièrement basée sur la manipulation émotionnelle.

Points centraux :

* Choix crucial : infiltration silencieuse ou révélation publique
* Découverte du **Nœud**, système de contrôle émotionnel
* Deux voies : briser les illusions ou infiltrer les souterrains
* Boss final : **Seren Taal**, ancienne capitaine du Vigilant devenue tyran

La chute de Seren Taal unit les planètes rebelles.

---

## 🌍 **MONDE 4 — NOVA TERRA : Le Monde Promis**

Dernière planète, habitable et fertile — destination originelle du Vigilant.

Points centraux :

* Exploration d’une station orbitale antique (optionnelle)
* Atterrissage sur un monde paradisiaque
* Serments des peuples unis : Eridani, Velyra, Aurelion
* Dernier choix : devenir dirigeant… ou refuser le pouvoir

Fin : **renaissance de l’humanité sur Nova Terra**.

---

# 🕹️ Commandes du jeu

| Commande            | Description             |
| ------------------- | ----------------------- |
| `observer`          | Décrit la zone actuelle |
| `aller <direction>` | Se déplacer (N/S/E/O)   |
| `retour`            | Déplace zone précédente |
| `prendre <objet>`   | Ramasser un objet       |
| `jeter <objet>`     | jette un objet          |
| `utiliser <objet>`  | Utiliser un objet       |
| `inventaire`        | Afficher l’inventaire   |
| `parler <nom>`      | Parler à un PNJ         |
| `attaquer <ennemi>` | Lancer un combat        |
| `examiner <objet>`  | Examiner un objet       |
| `quitter`           | Quitter le jeu          |
| `ai`                | Stats de réponses       |
| `historique`        | Affiche l'historique    |
| `statut`            | Affiche les pv, atk...  |


---

# 📁 Structure du projet

```
TBA_StellarRebellion/
│
├── game.py          # Boucle principale
├── actions.py       # Actions joueur : regarder, parler, attaquer, etc.
├── command.py       # Parsing de commandes
├── room.py          # Salles / zones
├── player.py        # Stats et inventaire
├── enemy.py         # Système de combat
├── item.py          # Objets & descriptions
├── character.py     # PNJ
├── config.py        # Définition du monde 1 (villes)
└── ai_quiz.py       # Module d’IA optionnel
```

---

# 📌 Perspectives d’évolution

* Ajout des mondes 2, 3 et 4 dans le code
* Sauvegarde/chargement de partie
* Interface graphique
* Effets sonores

---

# 🏫 Crédits

Projet développé dans le cadre des Travaux Pratiques TBA — **ESIEE Paris**
**Auteurs :** Berkant Baskin & Saad El Outati
**Année :** 2025

---

# 🚀 FIN

Le Vigilant est prêt.
Le Système Epsilon attend son capitaine.

---


