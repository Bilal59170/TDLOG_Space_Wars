"""@package docstring
Fichier de configuration - Contient toutes les constantes d'exécution du programme

"""
import numpy as np
# ----- Constantes de jeu -----

FPS = 60
TPS = 2 * FPS
FRAME_TIME = 1 / FPS
TICK_TIME = 1 / TPS

FRAME_TICKS = int(FRAME_TIME / TICK_TIME)

SHIP_SIZE = 50

SPEED_FACTOR = 1

WIN_SIZE = np.array([1280, 720])
MAP_SIZE = WIN_SIZE * 2
BACKGROUND_COLOR = (1,1,1)

BITMAP_RATIO = 5
# ----- Partie Astéroïdes -----


ASTEROID_STATS = [
    [10, 10],  # Petit Astéroïde : 10 HP, 10 Ressources
    [50, 60],  # Moyen Astéroïde : 50 HP, 60 Ressources
    [200, 300],  # ...
    [1000, 2000],
]

ASTEROID_CLASS_PROBABILITIES = [0.5, 0.3, 0.15, 0.05]

# ----- Partie Astéroïdes -----
