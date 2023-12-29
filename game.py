"""@package docstring
Fichier où l'on intègre la boucle de jeu

Fait appel à l'UI pour l'affichage
L'instance de jeu est nommée game_state

"""

import config


import random
import time
from inspect import isclass
import numpy as np

import pyglet
from pyglet.window import key
from pyglet.window import mouse
from time import time

import sprites
from ship import Ship
from asteroids import Asteroid
from projectiles import Projectile
from enemies import Enemy

try:
    from numba import njit
except:
    print("Numba not installed, collisions will be slower")
    njit = lambda x : x
    
from collisions import *

from profiling import Profiler

profiler = Profiler()

class GameEvents:
    """
    Classe qui gère les événements du jeu
    Notamment : - Les fonctions à appeler à chaque x ticks => Fonction each
                - Les fonctions à appeler à chaque collision => Fonction on_collide

    Exemple d'utilisation :
        game = Game()
        @game.each(10)
        def my_function(game):
            print("Appelée tous les 10 ticks")
        @game.on_collide(Asteroid, Ship)
        def my_function(game, asteroid, ship):
            print("Appelée à chaque collision entre un astéroïde et un vaisseau")

        @game.on_collide(Asteroid, Asteroid, sym=True)
        def my_function(game, asteroid1, asteroid2):
            print("Appelée à chaque collision entre deux astéroïdes")

    
    Comportement (pas passer trop de temps dessus):
    @game.each(10) => Initialise une classe each qui prend en paramètre le nombre de ticks entre chaque appel de la fonction
    def ...        => Appelle la fonction __call__ de l'instance de classe each avec en paramètre la fonction à appeler
        
    """

    def __init__(self):
        # Liste des fonctions à appeler à chaque x ticks [(n_ticks, function)]
        self._each = []
        # Liste des fonctions à appeler à chaque collision [(object1, object2, sym, function)]
        self._on_collide = []


        # Utilisation de foncteurs que l'on utilise comme des décorateurs
        globals().update({'target' : self})

        class each:
            # Foncteur qui permet d'ajouter une fonction à appeler à chaque x ticks

            # Instance référencée par le foncteur (la partie)
            target = target

            def __init__(self, number):
                # Nombre de ticks entre chaque appel de la fonction
                self.number = number
                
            def __call__(self, function):
                # Fonction à appeler
                self.target._each.append((self.number, function))
                del self

        class on_collide:
            # Même principe que each
            target = target
            def __init__(self, object1, object2, sym = False):
                # object1 et object2 sont des classes ou des instances de classes
                # sym indique si la collision est symétrique (ex : collision entre deux astéroïdes) => Evite d'appeler deux fois la fonction
                self.object1 = object1
                self.object2 = object2
                self.sym = sym

            def __call__(self, function):
                self.target._on_collide.append((self.object1, self.object2, self.sym, function))

        self.each = each
        self.on_collide = on_collide
        
    @profiler.profile
    def handle_events(self):
        """ Fonction qui gère les événements, appelée à chaque tick, dans la boucle de jeu """

        # Appel des fonctions à appeler à chaque x ticks
        for number, function in self._each:
            if self.ticks % number == 0:
                function(self)
        
        # Appel des fonctions à appeler à chaque collision
                
        for object1, object2, sym, function in self._on_collide:
            
            # On récupère les instances des classes si object1 et object2 sont des classes, sinon on les laisse telles quelles car ce sont des instances
            # la fonction issubclass permet de savoir si une classe est une sous-classe d'une autre
            # ex : issubclass(Asteroid, Entity) => True
            # ex : issubclass(BigAsteroid, Asteroid) => True
            # la fonction isclass permet de savoir si un objet est une classe
            # ex : isclass(Asteroid) => True
            # ex : isclass(Asteroid()) => False
            object1 = [e for e in self.entities if issubclass(e.__class__, object1)] if isclass(object1) else [object1]
            object2 = [e for e in self.entities if issubclass(e.__class__, object2)] if isclass(object2) else [object2]

            # On teste les collisions entre les deux listes d'objets
            if not sym:
                for e1 in object1:
                    for e2 in object2:
                        # On évite de tester une collision entre un objet et lui-même
                        if not e1 is e2:
                            # On teste la collision
                            if e1.intersects(e2):
                                # On appelle la fonction
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

class Camera:
    """ Classe qui gère la caméra """
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

    time = 0          # Temps de jeu
    ticks = 0         # Ticks de jeu

    def __init__(self, profile = False):
        # Initialisation des classes parentes
        pyglet.event.EventDispatcher.__init__(self)
        GameEvents.__init__(self)

        self.window = pyglet.window.Window(*config.WIN_SIZE)
        self.batch = pyglet.graphics.Batch()

        # Variable qui indique si la partie est terminée
        self.game_ended = False
        self.tick = 0
        
        # Taille de la carte / caméra
        self.map_size = config.MAP_SIZE
        self.camera = Camera()

        # Création du joueur à un endroit aléatoire
        self.player = Ship([0,0],
            #[np.random.randint(0, config.MAP_SIZE[0]), np.random.randint(0, config.MAP_SIZE[1])],
            config.SHIP_SIZE,
            game_state=self,
            acceleration=config.SHIP_ACCELERATION,
            max_speed=config.SHIP_MAX_SPEED
        )
        
        # Initialisation des listes d'entités
        self.asteroids = []
        enemy = Enemy(np.array([config.MAP_SIZE[0] / 4, config.MAP_SIZE[1] / 4]),
                      size=30.,
                      acceleration=2.,
                      max_speed=2.,
                      engage_radius=300.,
                      caution_radius=200.,
                      game_state=self)
        
        self.enemies = [enemy]
        
        self.entities = self.enemies

        # Ajout du joueur à la liste d'entités
        self.add_entity(self.player)
        
        # Permet de gérer les événements
        # Fonctionnement :
        # self.push_handlers(self.player) => Permet de gérer les événements liés au joueur
        # self.push_handlers(self) => Permet de gérer les événements liés à la partie
        # dans la classe dont on veut gérer les événements, on définit des fonctions de la forme on_xxx(self, ...), qui seront appelées à chaque événement xxx
        # ex : on_key_press(self, symbol, modifiers) => Appelée à chaque pression d'une touche du clavier
        # ex ici : on_close(self) => Appelée à chaque fermeture de la fenêtre
        self.window.push_handlers(self.player) 
        self.window.push_handlers(self)

        # Code de Broni
        self.time = 0
        self.old_time = time.time()

        self.keys = key.KeyStateHandler()
        self.window.push_handlers(self.keys)
        self.mousebuttons = mouse.MouseStateHandler()
        self.window.push_handlers(self.mousebuttons)

        self.mouse_x = 0
        self.mouse_y = 0

        self.profiling = profile
        if profile:
            profiler.open_plot()

        @self.window.event
        def on_mouse_motion(x, y, dx, dy):
            self.mouse_x, self.mouse_y = x, y

        @self.window.event
        def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
            if self.mousebuttons[mouse.RIGHT]:
                self.mouse_x, self.mouse_y = x, y



    def add_entity(self, object):
        # Ajoute un objet à la liste d'entités
        self.entities.append(object)
        if issubclass(object.__class__, Asteroid):
            self.asteroids.append(object)
        elif isinstance(object, Enemy):
            self.ennemies.append(object)

    def remove_entity(self, object):
        # Supprime un objet de la liste d'entités
        self.entities.remove(object)
        if issubclass(object.__class__, Asteroid):
            self.asteroids.remove(object)
        elif isinstance(object, Enemy):
            self.ennemies.remove(object)
            
    def update_speed(self):
        t = time.time() - self.old_time
        self.old_time = time.time()
        
        if (self.keys[key.Z] or self.keys[key.UP]) and (abs(self.player.speed[1]) < self.player.max_speed or self.player.speed[1] < 0):
            self.player.speed += t*self.player.acceleration*np.array([0., 1.])
        if (self.keys[key.Q] or self.keys[key.LEFT]) and (abs(self.player.speed[0]) < self.player.max_speed or self.player.speed[0] > 0):
            self.player.speed += t*self.player.acceleration*np.array([-1., 0.])
        if (self.keys[key.S] or self.keys[key.DOWN]) and (abs(self.player.speed[1]) < self.player.max_speed or self.player.speed[1] > 0):
            self.player.speed += t*self.player.acceleration*np.array([0., -1.])
        if (self.keys[key.D] or self.keys[key.RIGHT]) and (abs(self.player.speed[0]) < self.player.max_speed or self.player.speed[0] < 0):
            self.player.speed += t*self.player.acceleration*np.array([1., 0.])


    @profiler.profile
    def display(self):
        # Fonction qui gère l'affichage de la fenêtre de jeu

        self.window.clear()

        batch = pyglet.graphics.Batch()            # On utilise un batch pour afficher les objets => Permet de gagner en performance en évitant de faire des appels à OpenGL à chaque objet
        pyglet.gl.glClearColor(*config.BACKGROUND_COLOR, 1) # Couleur de fond de la fenêtre

        # On dessine les objets
        for e in self.entities:
            # On gère les erreurs de dessin pour afficher clairement dans quelle classe il y a une erreur
            try:
                # On dessine l'objet
                e.draw(batch=batch)
            except:
                print("Error drawing : ", e.__class__.__name__)
                raise

        batch.draw()
        self.batch.draw()

        self.window.flip()

    def new_projectile(self):
        # Fonction qui gère le lancement de projectiles
        if self.mousebuttons[mouse.RIGHT]:
                self.entities.append(self.player.throw_projectile(20))

    @profiler.profile
    def update(self, *other):
        self.new_projectile()
        self.update_speed()

        self.time += config.TICK_TIME

        self.camera.center = self.player.pos
        #Cas de bordure où la caméra ne doit pas bouger 
        if self.player.border['UP']:
            self.camera.center[1] =  config.WIN_SIZE[1]/2
        if self.player.border['DOWN']:
            self.camera.center[1] =  config.MAP_SIZE[1]- config.WIN_SIZE[1]/2
        if self.player.border['LEFT']:
            self.camera.center[0] =  config.WIN_SIZE[0]/2
        if self.player.border['RIGHT']:
            self.camera.center[0] =  config.MAP_SIZE[0]- config.WIN_SIZE[0]/2

        for e in self.entities:
            e.tick()
            
        if self.ticks % config.FRAME_TICKS == 0:
            self.display()
    
    
    def run(self):
        # Boucle de jeu
        while not self.game_ended:
            # On gère les événements
            self.handle_events()
            # On gère les entités / l'affichage
            self.update()
            # On fait circuler les événements
            self.window.dispatch_events()
            
            if self.profiling:
                profiler.update_plot()
            
    # Evénement de quand on essaie de fermer la fenêtre => On quitte la boucle de jeu et la fenêtre
    def on_close(self):
        self.game_ended = True
        pyglet.app.exit()
