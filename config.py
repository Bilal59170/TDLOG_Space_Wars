"""@package docstring
Fichier de configuration - Contient toutes les constantes d'exécution du programme

"""

# ----- Constantes de jeu -----

FPS = 60
TPS = 2 * FPS
FRAME_TIME = 1 / FPS
TICK_TIME = 1 / TPS

SHIP_SIZE = 20

SPEED_FACTOR = 1

WIN_SIZE = [1280, 720]
MAP_SIZE = [1280, 720]


# ----- Partie Astéroïdes -----


ASTEROID_STATS = [
    [10, 10],  # Petit Astéroïde : 10 HP, 10 Ressources
    [50, 60],  # Moyen Astéroïde : 50 HP, 60 Ressources
    [200, 300],  # ...
    [1000, 2000],
]

ASTEROID_CLASS_PROBABILITIES = [0.5, 0.3, 0.15, 0.05]

# ----- Partie Astéroïdes -----
