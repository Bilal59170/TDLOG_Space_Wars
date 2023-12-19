"""
Fichier où l'on intègre la boucle de jeu
Fait appel à l'UI pour l'affichage
L'instance de jeu est nommée game_state

"""
import pyglet
from ship import Ship
import config
import numpy as np
from pyglet.window import key
import random
import time

from asteroids.asteroids import *

from inspect import isclass # Fonction pour déterminer si les variables sont des classes ou des instances de classes

from numba import njit
from collisions import *

class GameEvents:
    def __init__(self):
        self._each = []
        self._on_collide = []

        globals().update({'target' : self})

        class each:
            target = target
            def __init__(self, number):
                self.number = number
                
            def __call__(self, function):
                self.target._each.append((self.number, function))
                del self

        class on_collide:
            target = target
            def __init__(self, object1, object2, sym = False):
                self.object1 = object1
                self.object2 = object2
                self.sym = sym

            def __call__(self, function):
                self.target._on_collide.append((self.object1, self.object2, self.sym, function))

        self.each = each
        self.on_collide = on_collide
        
    def handle_functions(self):
        for number, function in self._each:
            if self.ticks % number == 0:
                function(self)
        for object1, object2, sym, function in self._on_collide:

            # Optimisation : Pour les polygones, on utilise de la vectorisation sur les vertices
            # print(issubclass(object1.__class__, sprites.Polygon), object2.__class__)
            # if isclass(object1) and issubclass(object1, sprites.Polygon):

            #     object1 = [e.vertices for e in self.entities if issubclass(e.__class__, object1)] if isclass(object1) else [object1.vertices]
            #     object2 = [e.vertices for e in self.entities if issubclass(e.__class__, object2)] if isclass(object2) else [object2.vertices]

            #     if not sym:
            #         for e1 in object1:
            #             for e2 in object2:
            #                 if not e1 is e2:
            #                     if polygonPolygonCollisionOptimized(e1, e2):
            #                         function(self, e1, e2)
            #                         print('HEY')
            #     else:
            #         # On évite de tester deux fois les collisions symétriques
            #         for i in range(len(object1)):
            #             for j in range(i+1, len(object2)):
            #                 e1 = object1[i]
            #                 e2 = object2[j]
            #                 if polygonPolygonCollisionOptimized(e1, e2):
            #                     function(self, e1, e2)
            #                     print('HEZ')

            # else:
            object1 = [e for e in self.entities if issubclass(e.__class__, object1)] if isclass(object1) else [object1]
            object2 = [e for e in self.entities if issubclass(e.__class__, object2)] if isclass(object2) else [object2]

            if not sym:
                for e1 in object1:
                    for e2 in object2:
                        if not e1 is e2:
                            if e1.intersects(e2):
                                function(self, e1, e2)
            else:
                # On évite de tester deux fois les collisions symétriques
                for i in range(len(object1)):
                    for j in range(i+1, len(object2)):
                        if not object1[i] is object2[j]:
                            e1 = object1[i]
                            e2 = object2[j]
                            if e1.intersects(e2):
                                function(self, e1, e2)

class Map:
    def __init__(self) -> None:
        self.size = config.MAP_SIZE

class Camera:
    def __init__(self) -> None:
        self.size = config.WIN_SIZE
        self.center = [0, 0]

class Game(pyglet.event.EventDispatcher, GameEvents):

    """ 
    Classe principale du jeu

    Attributs : 
    - endgame : booléen qui indique si la partie est terminée
    - map : instance de la classe Map
    - player : instance de la classe Ship
    - asteroids : liste d'instances de la classe Asteroid
    - ennemies : liste d'instances de la classe Ennemy
    - entities : liste d'instances de la classe Entity
    - batch : batch d'objets
    - time : ticks de jeu
    - window : fenêtre pyglet

    Méthodes :
    - remove : supprime un objet de la liste d'entités
    - display : affiche la fenêtre de jeu
    - update : met à jour les entités
    - run : lance la boucle de jeu

    Méthodes de gestion des événements :
    - on_close : ferme la fenêtre de jeu
    - on_key_press : gère les événements liés aux touches du clavier
    
    
    """

    def __init__(self):
        pyglet.event.EventDispatcher.__init__(self)
        GameEvents.__init__(self)

        self.endgame = False
        self.map = Map()
        self.camera = Camera()

        self.player = Ship(
            np.array([0, 0]),
            config.SHIP_SIZE,
            game_state=self
        )
        
        self.asteroids = []
        self.ennemies = []
        self.entities = []
        self.batch = pyglet.graphics.Batch()
        self.tick = 0
        
        self.window = pyglet.window.Window(*config.WIN_SIZE)
        #push handler permet de ne pas utiliser de décorateur @windows.evnt. la fonction qui est appelée 
        # est on_key_press. Lorsqu'on décide de fermer la fenêtre, la fonction on_close s'execute
        self.window.push_handlers(self.player) 
        self.window.push_handlers(self)


        self.images = [] # TEST A SUPPRIMER ME LE RAPPELER SI BESOIN

        self.add_entity(self.player)

    def add_entity(self, object):
        self.entities.append(object)
            
        if isinstance(object, sprites.Image):
            self.images.append(object)
        if issubclass(object.__class__, Asteroid):
            self.asteroids.append(object)
        # elif isinstance(object, Ennemy):
        #     self.ennemies.append(object)


    def remove(self, object):
        pass

    t = time.time()
    frame_counter = 0
    FPS = 0
    time = 0
    ticks = 0

    def display(self):
        batch = pyglet.graphics.Batch()
        pyglet.gl.glClearColor(*config.BACKGROUND_COLOR, 1) # Set the background color
        for e in self.entities:
            try:
                e.draw(batch=batch)
            except:
                print("Error drawing : ", e.__class__.__name__)
                raise

        pyglet.text.Label('FPS : ' + str(self.FPS),
                                font_name='Times New Roman',
                                font_size=36,
                                color=(255,0,0,255),
                                x=10, y=10, batch=batch)

        batch.draw()
        self.batch.draw()

        self.frame_counter += 1
        dt = time.time()-self.t
        if dt > 1:
            self.FPS =  int(self.frame_counter / dt)
            self.frame_counter = 0
            self.t = time.time()
        

    def update(self):
        self.time += config.TICK_TIME
        self.ticks += 1
        #Rajouter condition où la cam ne doit pas bouger: cas on est à la bordure
        self.camera.center = self.player._pos
        for e in self.entities:
            e.tick()
        #if self.ticks % config.FRAME_TICKS == 0:
        if True:
            self.window.clear()
            self.display()
    
    
    def run(self):
        while not self.endgame:
            self.handle_functions()
            self.update()
            self.window.dispatch_events()
            self.window.flip()
            if self.endgame:
                break


    def on_close(self):
        self.endgame = True
        pyglet.app.exit()

    
    def on_key_press(self, symbol, modifiers):
        if symbol == key.Z or symbol == key.UP:
            self.player.speed = np.array([0, 1])*3
        elif symbol == key.Q or symbol == key.LEFT:
            self.player.speed = np.array([-1, 0])*3
        elif symbol == key.S or symbol == key.DOWN:
            self.player.speed = np.array([0, -1])*3
        elif symbol == key.D or symbol == key.RIGHT:
            self.player.speed = np.array([1, 0])*3
    

