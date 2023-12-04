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

from config import *
from utils import *

from typing import Any
from abc import ABC, abstractmethod

from shapely.geometry import Polygon as Poly

from pyglet.gl import *
import pyglet

import numpy as np
try:
    from numba import njit
except:
    njit = lambda x:x


class NoGameStateError(Exception):
    """Exception levée lorsqu'un objet n'a pas d'attribut game_state"""

    def __init__(self, object):
        super().__init__("No game state attributed to : {}".format(object))

class NullMap:
    def __init__(self):
        self.size = (0,0)
        self.center = (0,0)

class Entity:

    def __init__(self, pos, speed, game_state=None):
        self._pos = np.array(pos)
        self.speed = np.array(speed)

        # Peut-être trop générique
        self.has_game_state = False
        if game_state is not None:
            self._game_state = game_state
            self.map = game_state.map
            self.has_game_state = True
        else:
            self.map = NullMap()

    @property
    def pos(self):
        return np.array(
            [self._pos[0] % self.map.size[0], self._pos[1] % self.map.size[1]]
        )

    @pos.setter
    def pos(self, pos):
        self._pos = pos

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

    """ Propriétés de positions x/y"""

    @property
    def screen_x(self):
        return self.screen_pos[0]

    @property
    def screen_y(self):
        return self.screen_pos[1]

    @property
    def x(self):
        return self.pos[0]

    @property
    def y(self):
        return self.pos[1]

    @property
    def game_state(self):
        if self.has_game_state:
            return self._game_state
        raise NoGameStateError(self)

    def tick(self):
        self.pos += self.speed

class Sprites(ABC):
    """ Interface pour les sprites """
    @abstractmethod
    def draw(self):
        pass
    @abstractmethod
    def intersects(self, other):
        pass

# On utilise numba pour gagner en rapidité
@njit
def check_overlap(mask1, mask2, dx, dy):
    """Fonction qui teste si deux masques se superposent avec un décalage dx, dy"""
    height, width = mask1.shape

    for i in range(height):
        for j in range(width):
            new_i = i + dy # pixel correspondant dans l'autre image
            new_j = j + dx

            if 0 <= new_i < height and 0 <= new_j < width:
                if mask1[i, j] and mask2[new_i, new_j]:
                    return True

    return False

def get_sprite_mask(sprite):
    img_data = sprite.image.get_image_data()
    if img_data.format == "RGBA":
        i = img_data.get_data('RGBA', sprite.width*4)
        alpha = np.frombuffer(i, dtype=np.uint8)[::4].astype(bool).reshape(sprite.height, sprite.width)[::BITMAP_RATIO, ::BITMAP_RATIO]
    else:
        dims = np.ceil([sprite.width/5, sprite.height/5])
        return np.ones(dims, dtype=bool)
    return alpha

class BitmapSprite(Entity, Sprites):
    def __init__(self, pos, speed,
                 image,
                 theta=None,
                 game_state=None,
                 use_mask=True,
                 rotates_often=True):
        
        super().__init__(pos, speed, game_state=game_state)
        
        if game_state is not None:
            self.sprite = pyglet.sprite(image, x=Entity.screen_x, y=Entity.screen_y, batch=game_state.batch)
            self.inBatch = True
        else:
            self.sprite = pyglet.sprite(image, x=Entity.screen_x, y=Entity.screen_y)
            self.inBatch = False

        self._theta = 0 if theta is None else theta
        self.sprite.update(rotation=self._theta)
        self.rotates_often = rotates_often

        if self.use_mask:
            self.mask = get_sprite_mask(self.sprite)
 

    @property
    def theta(self):
        return self._theta
    
    @theta.setter
    def set_theta(self, theta):
        self._theta = theta
        self.sprite.update(rotation=theta)
        if self.use_mask and not self.rotates_often:
            self.mask = get_sprite_mask(self.sprite)

    def draw(self):
        x, y = self.screen_pos
        self.sprite.update(x, y)
        if not self.inBatch:
            self.draw()

    def intersects(self, other):

        if not (self.screen_x < other.screen_x + other.sprite.width and
            self.screen_x + self.sprite.width > other.screen_x and
            self.screen_y < other.screen_y + other.sprite.height and
            self.screen_y + self.sprite.height > other.screen_y):
            return False  # Bounding boxes do not overlap
        
        if not self.use_mask:
            return True
        
        if self.use_mask and self.rotates_often:
            self.mask = get_sprite_mask(self.sprite)
        
        dx = int((self.screen_x - other.screen_x)/BITMAP_RATIO)
        dy = int((self.screen_y - other.screen_y)/BITMAP_RATIO)

        return check_overlap(self.mask, other.mask, dx, dy)


class PolygonSprite(Entity, Sprites):
    def __init__(self, pos, speed, vertices, color, game_state=None, theta=None):
        Entity.__init__(self, pos, speed, game_state=game_state)
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
        return self.screen_pos[:, np.newaxis] + self._vertices

    @property
    def polygon(self):
        return Poly((self.pos[:, np.newaxis] + self.vertices).transpose)
    
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

def nagonSprite(n, scale, color, theta=0):
    pos = [0, 0]
    speed = [0, 0]
    vertices = create_nagon_vertices(n, scale, theta = theta)
    
    return PolygonSprite(pos, speed, vertices, color)

