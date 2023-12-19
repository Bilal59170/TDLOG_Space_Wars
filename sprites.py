from shapely.geometry import Polygon as Poly

from entity import Entity
from pyglet.gl import *
glEnable(GL_BLEND)
import pyglet

import numpy as np
from config import *
from collisions import *

try:
    from numba import njit
except:
    njit = lambda x:x

class Sprites:
    """ 
    Interface pour les sprites
    
    GPT : un sprite est une représentation visuelle d'un élément du jeu, souvent une image ou une animation,
          qui peut être déplacée et manipulée de manière dynamique à l'écran.
    
    """

    def draw(self):
        raise NotImplementedError

    def collides(self, other):
        raise NotImplementedError



######### PARTIE IMAGES #########

# On utilise numba pour gagner en rapidité sur les calculs => on compile en C
@njit
def check_overlap(mask1, mask2, dx, dy):
    """ Fonction qui teste si deux masques se superposent avec un décalage dx, dy """
    height, width = mask1.shape

    for i in range(height):
        for j in range(width):
            new_i = i + dy # Pixel correspondant dans l'autre image
            new_j = j + dx

            if 0 <= new_i < height and 0 <= new_j < width:
                if mask1[i, j] and mask2[new_i, new_j]:
                    return True

    return False

# Compliqué à comprendre, mais permet de récupérer le masque d'une image, ie les pixels qui sont transparents
def get_sprite_mask(sprite):
    img_data = sprite.image.get_image_data()
    if img_data.format == "RGBA":
        i = img_data.get_data('RGBA', sprite.width*4)
        alpha = np.frombuffer(i, dtype=np.uint8)[::4].astype(bool).reshape(sprite.height, sprite.width)[::BITMAP_RATIO, ::BITMAP_RATIO]
    else:
        dims = np.ceil([sprite.width/5, sprite.height/5])
        return np.ones(dims, dtype=bool)
    return alpha

class Image(Entity, Sprites):
    """
    Sprite pour afficher une image

    Implémentations :
     => draw : affiche l'image
     => intersects : teste si l'image se superpose à un autre sprite
     => theta : angle de rotation de l'image

    """
    def __init__(self,
                pos,
                image,
                game_state,
                theta=None,
                speed = [0, 0],
                use_mask=True,
                rotates_often=False):
        
        super().__init__(pos, game_state, speed)

        if isinstance(image, pyglet.sprite.Sprite):
            self.sprite = image
            image.x = self.screen_x
            image.y = self.screen_y
            image.batch = game_state.batch
        
        elif isinstance(image, pyglet.image.AbstractImage):
            self.sprite = pyglet.sprite.Sprite(img=image, x=self.screen_x, y=self.screen_y, batch=game_state.batch)
        
        elif type(image) == str:
            self.sprite = pyglet.sprite.Sprite(img=pyglet.image.load(image), x=self.screen_x, y=self.screen_y, batch=game_state.batch)
        
        else:
            raise ValueError("image must be a pyglet.sprite.Sprite, a pyglet.image.AbstractImage or a path to an image")

        self._theta = 0 if theta is None else theta
        self.sprite.update(rotation=self._theta)
        self.rotates_often = rotates_often
        self.use_mask = use_mask

        if self.use_mask:
            self.mask = get_sprite_mask(self.sprite)


    @property
    def theta(self):
        return self._theta
    
    @theta.setter
    def theta(self, theta):
        self._theta = theta
        self.sprite.update(rotation=theta)
        if self.use_mask and not self.rotates_often:
            self.mask = get_sprite_mask(self.sprite)

    def draw(self, batch=None):
        x, y = self.screen_pos
        self.sprite.update(x, y)
        self.sprite.draw()

    @property
    def bounds(self):
        return self.screen_x, self.screen_y, self.screen_x + self.sprite.width, self.screen_y + self.sprite.height


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


######### PARTIE POLYGONES #########

class Polygon(Entity, Sprites):
    """
    Sprite pour afficher un polygone

    Implémentations :
        => draw : affiche le polygone
        => intersects : teste si le polygone se superpose à un autre sprite
        => theta : angle de rotation du polygone

    """
    def __init__(self, pos, vertices, game_state, lineWidth=1, theta=None, fillColor=None, edgeColor=None, speed=[0, 0]):
        
        if fillColor is None and edgeColor is None:
            raise ValueError("Either fillColor or edgeColor must be specified")
        
        Entity.__init__(self, pos, game_state, speed=speed)

        self._vertices = np.array(vertices)

        if theta is not None:
            self._theta = theta
            self.rotation_matrix = np.array([
                [np.cos(theta), np.sin(theta)],
                [-np.sin(theta), np.cos(theta)],
            ])
    
        self.fillColor = fillColor
        self.edgeColor = edgeColor
        self.lineWidth = lineWidth

        self.boundingRadius = np.max(np.linalg.norm(self._vertices, axis=1))


    @property
    def theta(self):
        return self._theta
    
    @theta.setter
    def theta(self, theta):
        self._theta = theta
        self.rotation_matrix = np.array([
                [np.cos(theta), np.sin(theta)],
                [-np.sin(theta), np.cos(theta)],
            ])

    @property
    def vertices(self):
        if hasattr(self, 'theta'):
            return self.screen_pos + self._vertices @ self.rotation_matrix
        return self.screen_pos + self._vertices
    
    @property
    def bounds(self):
        return np.min(self.vertices, axis=0)[0], np.min(self.vertices, axis=0)[1], np.max(self.vertices, axis=0)[0], np.max(self.vertices, axis=0)[1]
    
    def intersects(self, other):
        if isinstance(other, Polygon):
            if self.boundingRadius + other.boundingRadius < np.linalg.norm(self.pos - other.pos):
                return False
            return polygonPolygonCollisionOptimized(self.vertices, other.vertices)
        elif isinstance(other, Circle):
            return polygonCircleCollision(self.vertices, other.pos, other.radius)
        elif isinstance(other, Image):
            return other.intersects(self)
        raise ValueError("Collision not implemented")
    
    def draw(self, batch = None):
        batch = None
        vertices = self.vertices.astype(int)

        useBatch = batch is None

        if batch is None:
            batch = pyglet.graphics.Batch()

        n = len(vertices)


        if self.fillColor is not None:
            colorType = 'c3B' if len(self.fillColor) == 3 else 'c4B'
            batch.add(n, pyglet.gl.GL_POLYGON, None,
                            ('v2f', vertices.reshape(-1)),
                            (colorType, self.fillColor * n))
            
        
        if self.edgeColor is not None:
             colorType = 'c3B' if len(self.edgeColor) == 3 else 'c4B'
             glLineWidth(self.lineWidth)
             batch.add(n, pyglet.gl.GL_LINE_LOOP, None,
                             ('v2f', vertices.reshape(-1)),
                             (colorType, self.edgeColor * n))

        if useBatch:
            batch.draw()

class Circle(Entity, Sprites):
    """
    Sprite pour afficher un cercle

    Implémentations :
        => draw : affiche le cercle
        => intersects : teste si le cercle se superpose à un autre sprite

    """
    def __init__(self, pos, radius, game_state, fillColor=None, edgeColor=None, lineWidth=1, speed=[0, 0]):
        Entity.__init__(self, pos, game_state, speed=speed)
        self.radius = radius
        self.fillColor = fillColor
        self.edgeColor = edgeColor
        self.lineWidth = lineWidth

    def intersects(self, other):
        if isinstance(other, Polygon):
            return polygonCircleCollision(other.vertices, self.pos, self.radius)
        elif isinstance(other, Circle):
            return np.linalg.norm(self.pos - other.pos) < self.radius + other.radius
        elif isinstance(other, Image):
            return other.intersects(self)
        raise ValueError("Collision not implemented")
    
    def bounds(self):
        return self.screen_x - self.radius, self.screen_y - self.radius, self.screen_x + self.radius, self.screen_y + self.radius

    def draw(self, batch=None):
        useBatch = batch is None

        if batch is None:
            batch = pyglet.graphics.Batch()

        if self.fillColor is not None:
            circle =  pyglet.shapes.Circle(self.screen_x, self.screen_y, self.radius, color=self.fillColor, batch = batch)

        
        if self.edgeColor is not None:
            pyglet.gl.glLineWidth(self.lineWidth)
            arc = pyglet.shapes.Arc(self.screen_x, self.screen_y, self.radius, color=self.edgeColor, batch = batch)

        if useBatch:
            batch.draw()
