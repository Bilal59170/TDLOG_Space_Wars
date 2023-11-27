"""@package docstring
Classe entité, dont hérite les projectiles, astéroïdes, le vaisseau, et les ennemis

Les différentes classes héritant de celle-ci ont toutes diverses méthodes :

- Affichage sur l'UI
    => Nom : display(self, game_state)
- Méthode de tick
    => Nom : tick(self, game_state)


Propriétés :
- Les coordonnées X et Y
- Sa vitesse

Méthodes:
- tick: pour bouger l'entité
- set_game_state : pour attribuer une instance de jeu à l'objet

"""

import numpy as np


class Entity:
    def __init__(self, pos, speed, game_state=None):
        self._pos = np.array(pos)
        self.speed = np.array(speed)

    @property
    def pos(self):
        return np.array(self._pos)

    @pos.setter
    def pos(self, pos):
        self._pos = pos

    @property
    def x(self):
        return self.pos[0]

    @property
    def y(self):
        return self.pos[1]

    def tick(self):
        self.pos += self.speed
