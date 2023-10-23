"""
Implémentation des astéroïdes

Propriétés d'un astéroïde :
- Sa taille, size
- Son apparence (forme couleur)
- Ses points de vie => (HP)
- Ses ressources => ressources


Méthodes d'un astéroïde :
 Méthodes entités => display, tick

"""

import numpy as np

from entity import Entity
from config import *

class Asteroid(Entity):

    def __init__(self, pos, speed, orientation, size, HP, ressources, asteroid_class):
        super().__init__(pos, speed)
        self.orientation = orientation
        self.size = size

        self._HP = HP
        self.ressources = ressources
        self.asteroid_class = asteroid_class


    def get_polygon(self):

        polygon_order = self.asteroid_class + 3 # Nombre de points du polygone => Un petit astéroide est un triangle, moyen un carré, ...
        angles = np.linspace(0, polygon_order, polygon_order + 1) / polygon_order
        angles = 2 * np.pi * angles[:-1] + self.orientation

        x_coordinates = self.screen_x + self.size * np.cos(angles)
        y_coordinates = self.screen_y + self.size * np.sin(angles)

        return x_coordinates, y_coordinates
    
    def tick(self):
        pass

    def die(self):
        """ Mort de l'astéroïde. Rapporte des ressources au joueur """
        pass

    @property
    def HP(self):
        return self._HP
    
    @HP.setter
    def HP(self, value):
        if value < 0:
            self.die()
        self._value = value

def get_random_asteroid():
    # Classe d'astéroïde => De 0 à 3
    asteroid_class = np.random.choice(range(4), p = ASTEROID_CLASS_PROBABILITIES)
    # Les statistiques qui correspondent
    stats = ASTEROID_STATS[asteroid_class]

