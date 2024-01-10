"""@package docstring
Fichier où l'on intègre la boucle de jeu

Fait appel à l'UI pour l'affichage
L'instance de jeu est nommée game_state

"""

import random
import time
from inspect import isclass
import numpy as np

import pyglet
from pyglet.window import key
from pyglet.window import mouse
from time import time, sleep

from game_engine import config, sprites
from game_engine.collisions import *
from game_engine.profiling import Profiler

from game_objects.ship import Ship
from game_objects.asteroids import Asteroid
from game_objects.projectiles import Projectile
from game_objects.enemies import Enemy
from game_objects.animations import XPLosion

from game_functions import game_static_display

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
        # Liste des fonctions à appeler à chaque affichage
        self._on_draw = []


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

    
    def on_draw(self, function):
        self._on_draw.append(function)
        return function
        
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
    def __init__(self, win_size) -> None:
        self.size = np.array(win_size)
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

    score_steps = [1000, 5000, 10000, 20000]
    step = 0

    def __init__(self, profile = False):
        # Initialisation des classes parentes
        pyglet.event.EventDispatcher.__init__(self)
        GameEvents.__init__(self)

        screen = pyglet.canvas.Display().get_default_screen()
        screen_dims = [screen.width, screen.height]
        del screen

        if config.FULLSCREEN:
            self.window = pyglet.window.Window(*screen_dims, fullscreen=True)
            self.win_size = screen_dims

        else:
            # On centre la fenêtre
            self.window = pyglet.window.Window(*config.WIN_SIZE, resizable=True)
            self.window.set_location(int(self.window.screen.width/2 - self.window.width/2), int(self.window.screen.height/2 - self.window.height/2))
            self.win_size = config.WIN_SIZE

        self.window.set_mouse_visible(True)
        self.window.set_caption("Space Wars")
        self.window.set_vsync(True ) #synchronise les fps du jeu avec les fps de l'écran de l'ordi 
        #self.window.set_icon(pyglet.image.load("ressources/icon.png")) => A ajouter quand on aura une icone
        
        self.batch = pyglet.graphics.Batch()

        # Variable qui indique si la partie est terminée
        self.game_ended = False
        self.tick = 0
        
        # Taille de la carte / caméra
        self.map_size = config.MAP_SIZE
        self.camera = Camera(self.win_size)

        # Création du joueur à un endroit aléatoire
        self.player = Ship(
            [np.random.randint(0, config.MAP_SIZE[0]), np.random.randint(0, config.MAP_SIZE[1])],
            game_state=self,
        )
        self.score = 0
        #Position finale du vaisseau quand il meurt. 
        #Utile pour afficher des animation quand on veut enlever le vaisseau du jeu une fois mort 
        self.final_player_pos = np.array([0, 0]) 
        self.player_dead = "Alive"

        # Initialisation des listes d'entités
        self.asteroids = []
        self.enemies = []
        self.entities = []
        """
        positions = []
        for i in range(5):
            positions.append(np.array([random.random()*config.MAP_SIZE[0], random.random()*config.MAP_SIZE[1]]))
        
        self.enemies = [Enemy(position,game_state=self) for position in positions]
        
        self.entities = []
        self.entities += self.enemies
        """

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
        self.old_time = time()
        self.tick_time = 0

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

    def add_score(self, score):
        self.score += score
        print(f'Score : {self.score}')

    def add_entity(self, object):
        # Ajoute un objet à la liste d'entités
        self.entities.append(object)
        if issubclass(object.__class__, Asteroid):
            self.asteroids.append(object)
        elif isinstance(object, Enemy):
            self.enemies.append(object)

    def remove_entity(self, object):
        # Supprime un objet de la liste d'entités
        if object in self.entities:
            self.entities.remove(object)
            if issubclass(object.__class__, Asteroid):
                self.asteroids.remove(object)
            elif isinstance(object, Enemy):
                self.enemies.remove(object)
            
    def update_speed(self):
        t = time() - self.old_time
        self.old_time = time()
        
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
        
        batch = pyglet.graphics.Batch()

        pyglet.gl.glClearColor(*config.BACKGROUND_COLOR, 1) # Couleur de fond de la fenêtre

        # On dessine les objets
        for e in self.entities:
            # On gère les erreurs de dessin pour afficher clairement dans quelle classe il y a une erreur
            if hasattr(e, 'is_on_screen'):
                if not e.is_on_screen():
                    continue

            try:
                # On dessine l'objet
                e.draw(batch=batch)
            except:
                print("Error drawing : ", e.__class__.__name__)
                raise
                #Affichage de la map et de la position du ship
             
        mult_factor_win = 1/10
        mult_factor_map_win = config.MAP_SIZE / config.WIN_SIZE
        gap = 10 #espace entre la map et la bordure de la fenêtre

        #Point en haut à gauche du carré

        little_map_coord = np.array([
            (1-mult_factor_win)*config.WIN_SIZE[0] - gap,
            (1-mult_factor_win)*config.WIN_SIZE[1] - gap])
        
        ship_little_map_coord = little_map_coord + np.array([
            self.player.x / mult_factor_map_win[0] * mult_factor_win,
            self.player.y / mult_factor_map_win[1] * mult_factor_win])
        
        little_cam_coord = little_map_coord + np.array([
            (self.camera.center[0]-self.camera.size[0]/2) / mult_factor_map_win[0] * mult_factor_win,
            (self.camera.center[1]-self.camera.size[1]/2) / mult_factor_map_win[1] * mult_factor_win,
        ])
        
        little_map = pyglet.shapes.BorderedRectangle(
            x = little_map_coord[0],
            y = little_map_coord[1], 
            width = mult_factor_win*config.WIN_SIZE[0], 
            height = mult_factor_win*config.WIN_SIZE[1],
            border = 5,
            color = (200, 200, 200),
            border_color = (0, 0, 0),
            batch = batch)
        
        little_cam = pyglet.shapes.BorderedRectangle(
            x = little_cam_coord[0],
            y = little_cam_coord[1], 
            width = mult_factor_win*config.WIN_SIZE[0]/ mult_factor_map_win[0], 
            height = mult_factor_win*config.WIN_SIZE[1]/ mult_factor_map_win[1],
            border = 1,
            color = (255, 255, 255),
            border_color = (0, 0, 0),
            batch = batch)
        

        little_point = pyglet.shapes.Circle(
            x = ship_little_map_coord[0],
            y = ship_little_map_coord[1],
            radius = 5,
            color = (0, 255, 0)
        )

        
        # little_point = pyglet.shapes.Circle(self.player.screen_x ,5, color = (255, 0, 0), batch = batch)
        batch.draw()
        self.batch.draw()
        little_point.draw()

        for function in self._on_draw:
            function(self)

        game_static_display(self)
        
        self.window.flip()


    def hurt_animation(self):
        # Fonction qui fait une transition entre la couleur blanche, rouge, verte et blanche
        rgb_func = lambda x : (1 , 1- 4*x*(1-x)/2, 1- 4*x*(1-x)/2)

        if self.player.is_invicible:
            x = self.player.timer_invicible / self.player.invicible_time
            pyglet.gl.glClearColor(*rgb_func(x), 1)


    def new_projectile(self):
        # Fonction qui gère le lancement de projectiles
        if self.mousebuttons[mouse.RIGHT]:
            #self.entities.append(self.player.throw_projectile())
            P = self.player.shoot()
            if P != None:
                self.entities.append(P)
        for enemy in self.enemies:
            P = enemy.shoot(self.player)
            if P != None:
                self.entities.append(P)


    @profiler.profile
    def update(self, *other):
        self.new_projectile()
        self.update_speed()

        self.time += config.TICK_TIME

        if self.step < len(self.score_steps):
            if self.score >= self.score_steps[self.step]:
                self.step += 1
                self.player.update_step()

        if (self.player_dead == "Alive"):
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
        elif(self.player_dead == "Dead"):
            self.final_player_pos = self.player.die()
            self.remove_entity(self.player)
            self.player_dead = "Gone"
            XPLosion(self.final_player_pos, self)
            

        for e in self.entities:
            e.tick()
            
        if self.ticks % config.FRAME_TICKS == 0:
            self.display()

        # On attend le temps restant pour avoir un tick toutes les config.TICK_TIME secondes
        # On calcule le temps restant en secondes
        time_to_wait = config.TICK_TIME - (time() - self.tick_time)
        # On attend le temps restant
        if time_to_wait > 0:
            sleep(time_to_wait)
        # On met à jour le temps de tick
        self.tick_time = time()
        # On incrémente le nombre de ticks
        self.ticks += 1

    
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

    def on_resize(self, width, height):
        self.win_size = [width, height]
        self.camera.size = np.array([width, height])
