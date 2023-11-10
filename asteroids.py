import numpy as np

from entity import Entity
from config import *


class Asteroid(Entity):
    (
        """
    Asteroid(Entity) :

    Une classe pour créer un astéroïde, sorte de punching ball qui une fois détruit donne des ressources au joueur

    ...

    Attributs
    ----------
    orientation : float
        angle de l'astéroïde
    size : float
        taille de l'astéroïde
    hp : float
        points de vie
    ressources : float
        nombres de ressources que l'astéroïde apporte au joueur
    asteroid_class : int dans [0, 3]
        classe de l'astéroïde
            0 : petit astéroïde
            1 : moyen astéroïde
            2 : grand astéroïde
            3 : giga  astéroïde

    Méthodes
    --------
    get_polygon(self) : tuple[array]
        retourne un tuple qui contient les coordonnées x, y sur l'écran du polygone
    get_map_polygon(self) : tuple[array]
        retourne un tuple qui contient les coordonnées x, y sur la carte du polygone
    die :
        fait mourir l'astéroïde, donnant des ressources au joueur
    tick :
        pour gérer les déplacements / la régénération des PVs
    ===========
    Hérite de :
    """
        + Entity.__doc__
    )

    def __init__(self, pos, speed, orientation, size, HP, ressources, asteroid_class):
        super().__init__(pos, speed)
        self.orientation = orientation
        self.size = size

        self._HP = HP
        self.ressources = ressources
        self.asteroid_class = asteroid_class

    def create_polygon(self):
        polygon_order = (
            self.asteroid_class + 3
        )  # Nombre de points du polygone => Un petit astéroide est un triangle, moyen un carré, ...
        angles = np.linspace(0, polygon_order, polygon_order + 1) / polygon_order
        angles = 2 * np.pi * angles[:-1] + self.orientation

        x_coordinates = self.screen_x + self.size * np.cos(angles)
        y_coordinates = self.screen_y + self.size * np.sin(angles)

        return x_coordinates, y_coordinates

    def create_map_polygon(self):
        polygon_order = (
            self.asteroid_class + 3
        )  # Nombre de points du polygone => Un petit astéroide est un triangle, moyen un carré, ...
        angles = np.linspace(0, polygon_order, polygon_order + 1) / polygon_order
        angles = 2 * np.pi * angles[:-1] + self.orientation

        x_coordinates = self.map_x + self.size * np.cos(angles)
        y_coordinates = self.map_y + self.size * np.sin(angles)

        return x_coordinates, y_coordinates

    def tick(self):
        """
        Fonction de tick
            OPTIONNEL => Rajouter la régénération au bout d'un certain temps
        """
        super().tick()

    def die(self):
        """Mort de l'astéroïde. Rapporte des ressources au joueur"""
        self.game_instance.remove(self)

    @property
    def HP(self):
        return self._HP

    @HP.setter
    def HP(self, value):
        if value <= 0:
            self.die()
        self._value = value


def get_random_asteroid():
    # Classe d'astéroïde => De 0 à 3
    asteroid_class = np.random.choice(range(4), p=ASTEROID_CLASS_PROBABILITIES)
    # Les statistiques qui correspondent
    hp, resources = ASTEROID_STATS[asteroid_class]
