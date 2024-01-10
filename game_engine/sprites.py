from .entity import Entity
from pyglet.gl import *
import pyglet

import numpy as np
from .config import *
from .collisions import *

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
    
    def is_on_screen(self):
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

        self.isAnimated = False
        self.was_on_screen = False

        if isinstance(image, pyglet.sprite.Sprite):
            self.sprite = image
            image.x = self.screen_x
            image.y = self.screen_y
            image.batch = game_state.batch
        
        elif isinstance(image, pyglet.image.AbstractImage):
            self.sprite = pyglet.sprite.Sprite(img=image, x=self.screen_x, y=self.screen_y, batch=game_state.batch)
        
        elif isinstance(image, pyglet.image.Animation):
            print('LOADED ANIMATION')
            self.sprite = pyglet.sprite.Sprite(img=image.frames[0].image, x=self.screen_x, y=self.screen_y, batch=game_state.batch)
            self.isAnimated = True
            self.animation = image
            self.animation_index = 0
            self.animation_time = 0
            self.animation_duration = image.get_duration()
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

        if self.isAnimated:
            self.animation_index = 0
            time = self.animation_time % self.animation_duration
            while time > self.animation.frames[self.animation_index].duration:
                time -= self.animation.frames[self.animation_index].duration
                self.animation_index += 1
            self.sprite.image = self.animation.frames[self.animation_index].image

        self.sprite.update(x, y)


    @property
    def bounds(self):
        return self.screen_x, self.screen_y, self.screen_x + self.sprite.width, self.screen_y + self.sprite.height


    def intersects(self, other):

        if not isinstance(other, Image):
            raise ValueError("other must be an instance of Image")

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
    
    def is_on_screen(self):
        
        if self.screen_x < WIN_SIZE[0] and self.screen_y < WIN_SIZE[1] and self.screen_x + self.sprite.width > 0 and self.screen_y + self.sprite.height > 0:
            self.was_on_screen = True
            return True

        else:
            if self.was_on_screen:
                self.was_on_screen = False
                return True

            return False

    def tick(self):
        super().tick()
        if self.isAnimated:
            self.animation_time += TICK_TIME

######### PARTIE POLYGONES #########

class Polygon(Entity, Sprites):
    """
    Sprite pour afficher un polygone

    Implémentations :
        => draw : affiche le polygone
        => intersects : teste si le polygone se superpose à un autre sprite
        => theta : angle de rotation du polygone

    Paramètres :
        => pos : position du polygone sur la carte
        => vertices : tableau numpy des sommets du polygone
        => game_state : instance de GameState
        => lineWidth : largeur des bords du polygone
        => theta : angle de rotation du polygone
        => fillColor : couleur de remplissage du polygone
        => edgeColor : couleur des bords du polygone
        => speed : vitesse du polygone

    """
    def __init__(self, pos, vertices, game_state, lineWidth=1, theta=None, fillColor=None, edgeColor=None, speed=[0, 0]):
        
        if fillColor is None and edgeColor is None:
            raise ValueError("Either fillColor or edgeColor must be specified")
        
        Entity.__init__(self, pos, game_state, speed=speed)
        self._vertices = np.array(vertices)
        self.boundingRadius = np.max(np.linalg.norm(self._vertices, axis=1))
    
        self.fillColor = fillColor
        self.edgeColor = edgeColor
        self.lineWidth = lineWidth

        if theta is not None:
            self._theta = theta
            self.rotation_matrix = np.array([
                [np.cos(theta), np.sin(theta)],
                [-np.sin(theta), np.cos(theta)],
            ])

    @property
    def theta(self):
        return self._theta
    
    @theta.setter
    def theta(self, theta):
        # On met à jour la matrice de rotation quand on change l'angle
        self._theta = theta
        self.rotation_matrix = np.array([
                [np.cos(theta), np.sin(theta)],
                [-np.sin(theta), np.cos(theta)],
            ])

    @property
    def vertices(self):
        # On applique la rotation si elle existe pour obtenir les sommets du polygone à l'écran
        if hasattr(self, 'theta'):
            return self.screen_pos + self._vertices @ self.rotation_matrix
        return self.screen_pos + self._vertices
    
    @property
    def bounds(self):
        return np.min(self.vertices, axis=0)[0], np.min(self.vertices, axis=0)[1], np.max(self.vertices, axis=0)[0], np.max(self.vertices, axis=0)[1]
    
    def intersects(self, other):
        return does_collide(self, other)
    
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

    def is_on_screen(self):
        # On approxime la taille du polygone par le diamètre du cercle circonscrit
        win_size = self.camera.size
        x, y = self.screen_pos
        return x + self.boundingRadius > 0 and x - self.boundingRadius < win_size[0] and y + self.boundingRadius > 0 and y - self.boundingRadius < win_size[1]

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
        return does_collide(self, other)
    
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
    
    def is_on_screen(self):
        return self.screen_x + self.radius > 0 and self.screen_x - self.radius < WIN_SIZE[0] and self.screen_y + self.radius > 0 and self.screen_y - self.radius < WIN_SIZE[1]


class Label(Entity):
    """
    
    Texte affiché sur la carte
    
    """

    def __init__(self, pos, text, game_state, font_size=12, font_name='Arial', color=(255, 255, 255, 255), anchor_x='center', anchor_y='center', speed=[0, 0]):
        Entity.__init__(self, pos, game_state, speed=speed)
        self.text = text
        self.font_size = font_size
        self.font_name = font_name
        self.color = color
        self.anchor_x = anchor_x
        self.anchor_y = anchor_y

    def draw(self, batch=None):
        useBatch = batch is None

        if batch is None:
            batch = pyglet.graphics.Batch()

        label = pyglet.text.Label(self.text, font_size=self.font_size, font_name=self.font_name, color=self.color, x=self.screen_x, y=self.screen_y, anchor_x=self.anchor_x, anchor_y=self.anchor_y, batch=batch)

        if useBatch:
            batch.draw()


def does_collide(sprite1, sprite2):
    """
    Fonction qui teste si deux sprites se superposent
    """

    assert isinstance(sprite1, Sprites) and isinstance(sprite2, Sprites), "sprite1 and sprite2 must be instances of Sprites"

    if isinstance(sprite1, Polygon) and isinstance(sprite2, Polygon):
        # On teste d'abord si les bounding boxes se superposent
        if sprite1.boundingRadius + sprite2.boundingRadius < np.linalg.norm(sprite1.pos - sprite2.pos):
            return False
        return does_polygons_collide(sprite1.vertices, sprite2.vertices)
    
    elif isinstance(sprite1, Polygon) and isinstance(sprite2, Circle):
        # On teste d'abord si les bounding boxes se superposent
        if sprite1.boundingRadius + sprite2.radius < np.linalg.norm(sprite1.pos - sprite2.pos):
            return False
        return polygonCircleCollision(sprite1.vertices, sprite2.pos, sprite2.radius)
    
    elif isinstance(sprite1, Circle) and isinstance(sprite2, Polygon):
        # On teste d'abord si les bounding boxes se superposent
        if sprite1.radius + sprite2.boundingRadius < np.linalg.norm(sprite1.pos - sprite2.pos):
            return False
        return polygonCircleCrossing(sprite2.vertices, sprite1.pos, sprite1.radius)
    
    elif isinstance(sprite1, Circle) and isinstance(sprite2, Circle):
        return np.linalg.norm(sprite1.pos - sprite2.pos) < sprite1.radius + sprite2.radius
    
    elif isinstance(sprite1, Image) and isinstance(sprite2, Image):
        return sprite1.intersects(sprite2)
    
    elif isinstance(sprite1, Image) and isinstance(sprite2, Polygon):
        raise ValueError("Image-Polygon collision not implemented")
    elif isinstance(sprite1, Polygon) and isinstance(sprite2, Image):
        raise ValueError("Image-Polygon collision not implemented")
    
    elif isinstance(sprite1, Image) and isinstance(sprite2, Circle):
        raise ValueError("Image-Circle collision not implemented")
    elif isinstance(sprite1, Circle) and isinstance(sprite2, Image):
        raise ValueError("Image-Circle collision not implemented")
    
        
from pyglet.event import EventDispatcher
class FixedButton(EventDispatcher):
    """ 
    Bouton clickable, à sous classer avec une méthode callback, qui sera appelée quand le bouton est cliqué
    Méthodes : 
        => draw : affiche le bouton
        => on_mouse_press : détecte si le bouton a été cliqué
    """

    pass