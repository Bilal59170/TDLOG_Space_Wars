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

class Map:
    def __init__(self) -> None:
        self.size = config.MAP_SIZE
        self.center = [config.MAP_SIZE[0]/2, config.MAP_SIZE[1]/2]

class Camera():
    def __init__(self) -> None:
        self.size = config.WIN_SIZE
        self.center = [config.MAP_SIZE[0]/2, config.MAP_SIZE[1]/2]

class Game(pyglet.event.EventDispatcher):

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
        super().__init__()
        self.endgame = False
        self.map = Map()
        self.camera = Camera()


        self.player = Ship(
            np.array([config.MAP_SIZE[0] / 2, config.MAP_SIZE[1] / 2]),
            config.SHIP_SIZE,
            game_state=self
        )
        
        self.asteroids = []
        self.ennemies = []
        self.entities = [self.player] + self.asteroids + self.ennemies
        self.batch = pyglet.graphics.Batch()
        self.time = 0
        
        self.window = pyglet.window.Window(*config.WIN_SIZE)
        #push handler permet de ne pas utiliser de décorateur @windows.evnt. la fonction qui est appelée 
        # est on_key_press. Lorsqu'on décide de fermer la fenêtre, la fonction on_close s'execute
        self.window.push_handlers(self.player) 
        self.window.push_handlers(self)


    def remove(self, object):
        pass

    t = time.time()
    frame_counter = 0
    FPS = 0

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

        self.frame_counter += 1
        dt = time.time()-self.t
        if dt > 1:
            self.FPS =  int(self.frame_counter / dt)
            self.frame_counter = 0
            self.t = time.time()
        

    def update(self):
        self.time += config.TICK_TIME
        #Rajouter condition où la cam ne doit pas bouger: cas on est à la bordure
        self.camera.center = self.player.pos
        for e in self.entities:
            e.tick()
        if self.time % config.FRAME_TIME:
            self.window.clear()
            self.display()
    
    
    def run(self):
        while not self.endgame:
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
    

