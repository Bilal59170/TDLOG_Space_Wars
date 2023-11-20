"""
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
from shapely.geometry import Polygon as Poly
from config import *
from pyglet.gl import *


class NoGameStateError(Exception):
    """Exception levée lorsqu'un objet n'a pas d'attribut game_state"""

    def __init__(self, object):
        super().__init__("No game state attributed to : {}".format(object))


class Entity:
    """
    Classe




    """

    def __init__(self, pos, speed, game_state=None):
        self._pos = np.array(pos)
        self._speed = np.array(speed)

        # Peut-être trop générique
        self.has_game_state = False
        if game_state is not None:
            self._game_state = game_state
            self._map = game_state.map
            self.has_game_state = True

    """ ==== PROPRIETES === """

    """ Propriétés sur la position des objets """

    @property
    def pos(self):
        return np.array(
            [self._pos[0] % self.map.size[0], self._pos[1] % self.map.size[1]]
        )

    @property
    def map_pos(self):
        return self.pos

    @property
    def screen_pos(self):
        """

        Dans cette fonction on adresse un problème aux bords. En effet, on pourrait penser que les coordonnées
        à l'écran, c'est juste les coordonnées sur la carte desquelles on retire le point sur lequel est centré
        la caméra. Mais en fait, ça dépend.

        Par exemple, si on imagine un point sur une carte qui est exactement 4 fois plus petite que l'écran latéralement
        et de la même longueur, le point va apparaître 4 fois si on veut une carte parfaitement torique ...

        On part sur le principe que la fenêtre est plus petite que la carte

        """

        # Empêcher le cas où l'écran est plus grand que la map

        pos_0 = (self.pos - self.map.center).astype(
            int
        )  # Position 1 : Position normale
        pos_1 = (self.pos - self.map.center + self.map.size).astype(
            int
        )  # Position 2 : A gauche ou en bas
        x = (
            pos_0[0]
            if abs(pos_0[0] - WIN_SIZE[0] / 2) < abs(pos_1[0] - WIN_SIZE[0] / 2)
            else pos_1[0]
        )
        y = (
            pos_0[1]
            if abs(pos_0[1] - WIN_SIZE[1] / 2) < abs(pos_1[1] - WIN_SIZE[1] / 2)
            else pos_1[1]
        )

        return np.array([x, y]).astype(int)

    @pos.setter
    def pos(self, pos):
        self._pos = pos

    @map_pos.setter
    def map_pos(self, pos):
        # Contrôle d'accès
        self._pos = pos

    """ Vitesse """

    @property
    def speed(self):
        return self._speed

    @speed.setter
    def speed(self, speed):
        self._speed = speed

    """ Propriétés de positions x/y"""

    @property
    def screen_x(self):
        return self.screen_pos[0]

    @property
    def screen_y(self):
        return self.screen_pos[1]

    @property
    def map_x(self):
        return self.pos[0]

    @property
    def map_y(self):
        return self.pos[1]

    @property
    def x(self):
        return self.map_x

    @property
    def y(self):
        return self.map_y

    @x.setter
    @map_x.setter
    def x(self, x):
        self._pos[0] = x

    @y.setter
    @map_y.setter
    def y(self, y):
        self._pos[1] = y

    @property
    def game_state(self):
        if self.has_game_state:
            return self._game_state
        raise NoGameStateError(self)

    @property
    def map(self):
        if self.has_game_state:
            return self._map
        raise NoGameStateError(self)
    
    def tick(self):
        self.pos += self.speed

import pyglet

class Sprites(Entity, pyglet.sprite.Sprite):
    def __init__(self, chemin_image=None, polygone=None):
        """
        Classe d'un sprite
        => Implémente les collisions entre sprites
        => Implémente l'affichage sur l'écran
        => Peut être une image ou un polygone
        args : - Nom de fichier
               - Polygone sous forme de liste de points (x, y)
        """
        super(Entity).__init__()
        super(pyglet.sprite.Sprite).__init__()

    def intersects(self, other):
        """ Détermine si deux sprites sont en collision """
        pass

class BitmapSprite(Entity):
    def __init__(self, pos, speed, image, theta=None, game_state=None):
        super().__init__(pos, speed, game_state=game_state)
        if game_state is not None:
            self.sprite = pyglet.sprite(image, x=Entity.screen_x, y=Entity.screen_y, batch=game_state.batch)
            self.inBatch = True
        else:
            self.sprite = pyglet.sprite(image, x=Entity.screen_x, y=Entity.screen_y)
            self.inBatch = False
        self._theta = 0 if theta is None else theta
        self.sprite.update()

    @property
    def theta(self):
        return self._theta
    
    @theta.setter
    def set_theta(self, theta):
        self._theta = theta
        self.sprite.update(rotation=theta)

    def draw(self):
        x, y = self.screen_pos
        self.sprite.update(x, y)
        if not self.inBatch:
            self.draw()

    def intersects(self, other):






class PolygonSprite(Entity):
    def __init__(self, pos, speed, vertices, color, game_state=None, theta=None):
        Entity.__init__(pos, speed, game_state=game_state)
        self._vertices = np.array(vertices)
        self.color = color
        if theta is not None:
            self._theta = theta
            self.rotation_matrix = np.array([
                [np.cos(np.pi / 2 - theta), np.sin(np.pi / 2 - theta)],
                [-np.sin(np.pi / 2 - theta), np.cos(np.pi / 2 - theta)],
            ])
    
    @property
    def theta(self):
        return self._theta
    @theta.setter
    def set_theta(self, theta):
        self._theta = theta
        self.rotation_matrix = np.array([
                [np.cos(np.pi / 2 - theta), np.sin(np.pi / 2 - theta)],
                [-np.sin(np.pi / 2 - theta), np.cos(np.pi / 2 - theta)],
            ])
    

    @property
    def vertices(self):
        if hasattr(self, 'theta'):
            return self.screen_pos + self.rotation_matrix @ self._vertices
        return self.screen_pos + self._vertices

    @property
    def polygon(self):
        return Poly(self.pos + self.vertices)
    
    def intersects(self, other):
        if isinstance(other, PolygonSprite):
            return self.polygon.intersects(other.polygon)    
        else:
            raise ValueError("Collision not implemented")
    
    def draw(self):
        pyglet.gl.glColor3ub(*self.color)
        vertices = self.vertices
        pyglet.graphics.draw(len(vertices),
                             pyglet.gl.GL_POLYGON,
                             ('v2f', (self.screen_pos + vertices).reshape(-1)),
                             ('c3B', self.color * len(vertices)))