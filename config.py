"""

Fichier de configuration - Contient toutes les constantes d'exécution du programme

"""

# ----- Constantes de jeu -----

FPS = 60
TICK_TIME = 1 / FPS

SPEED_FACTOR = 1

WIN_SIZE = [1280, 720]
MAP_SIZE = [12800, 7200]


# ----- Partie Astéroïdes -----


ASTEROID_STATS = [
    [10, 10],  # Petit Astéroïde : 10 HP, 10 Ressources
    [50, 60],  # Moyen Astéroïde : 50 HP, 60 Ressources
    [200, 300],  # ...
    [1000, 2000],
]

ASTEROID_CLASS_PROBABILITIES = [0.5, 0.3, 0.15, 0.05]

# ----- Partie Astéroïdes -----
