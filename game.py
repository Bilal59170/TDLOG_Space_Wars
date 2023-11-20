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

class Map:
    def __init__(self) -> None:
        self.size = config.MAP_SIZE
        self.center = [0,0]

class Game(pyglet.event.EventDispatcher):

    """ """

    def __init__(self):
        super().__init__()
        self.endgame = False
        self.map = Map()

        self.player = Ship(
            np.array([config.MAP_SIZE[0] / 2, config.MAP_SIZE[1] / 2]),
            np.array([0, 0]),
            config.SHIP_SIZE,
            game_state=self
        )
        self.asteroids = []
        self.ennemies = []
        self.entities = [self.player] + self.asteroids + self.ennemies
        self.batch = []
        self.time = 0
        self.window = pyglet.window.Window(*config.WIN_SIZE)
        self.window.push_handlers(self.player)
        self.window.push_handlers(self)

    def remove(self, object):
        pass

    def display(self):
        pyglet.gl.glClearColor(*config.BACKGROUND_COLOR, 1)
        for e in self.entities:
            e.draw()

    def update(self):
        self.time += config.TICK_TIME
        for e in self.entities:
            e.tick()
        self.window.clear()
        if self.time % config.FRAME_TIME:
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
            self.player.speed = np.array([0, -1])
        elif symbol == key.Q or symbol == key.LEFT:
            self.player.speed = np.array([-1, 0])
        elif symbol == key.S or symbol == key.DOWN:
            self.player.speed = np.array([0, 1])
        elif symbol == key.D or symbol == key.RIGHT:
            self.player.speed = np.array([1, 0])
    

game = Game()
game.run()