"""
    Scénario d'une partie :
    Génération initiale de terrain (skip for v1)
    Création du personnage joueur
    Affichage de la fenêtre
    game_time = 0

    Boucle principale de jeu (tant que l'utilisateur ne met pas fin au jeu, ou que vaisseau.PV > 0):
    game_time += TICK_TIMESTEP
    récupérer les événements : position de souris, clic
    game.tick() (for all entities in game: entity.tick())
    si game_time % FRAME_TIME == 0:
        affichage
"""

import config

from entity import Entity
import sprites
from game import Game


from asteroids.asteroids import *

# if __name__ == "__main__":  

#     game = Game()

#     pos = [0, 0]
#     speed = [0, 0]
#     vertices = create_nagon_vertices(5, 100)

#     asteroid = BigAsteroid([100, 100], game, theta=np.pi/6)
#     game.asteroids.append(asteroid)
#     game.entities.append(asteroid)

#     asteroid = SmallAsteroid([400, 400], game, theta=np.pi/6)
#     game.asteroids.append(asteroid)
#     game.   entities.append(asteroid)

#     asteroideTriangle = MediumAsteroid([0, 400], game, theta=np.pi/6)
#     game.asteroids.append(asteroideTriangle)
#     game.entities.append(asteroideTriangle)

#     masterAsteroid = MasterAsteroid([400, 0], game, theta=np.pi/6, speed=[.1, 0])
#     game.asteroids.append(masterAsteroid)
#     game.entities.append(masterAsteroid)

#     circle = sprites.Circle([0, 0], 100, game, fillColor=(255, 0, 0), edgeColor=(0, 0, 0), lineWidth=5)
#     game.entities.append(circle)

#     game.run()


""" LES TESTS DE BIL """


img_caca = pyglet.image.load("Sprites/caca.png")

if __name__ == "__main__":
    # game_window = pyglet.window.Window()

    # @game_window.event
    # def on_draw():
    #     # game_window.clear()
    #     sprite_caca.draw()        

    game = Game()

    caca = sprites.Image(np.array([config.MAP_SIZE[0] / 2, config.MAP_SIZE[1] / 2]), img_caca, game)
    caca2 = sprites.Image(np.array([config.MAP_SIZE[0] / 2 + 500, config.MAP_SIZE[1] / 2]), img_caca, game, speed=[-10, 0], theta=np.pi/6)

    game.add_entity(caca)
    game.add_entity(caca2)

    # @game.each(1)
    # def e(game):
    #     print('='*16)

    import random
    @game.each(5)
    def spawn_asteroids(game):
        if len(game.asteroids) > 20:
            return

        weights = [10, 20, 50]
        probabilities = [w/sum(weights) for w in weights]

        if random.random() < .2:
            for i in range(np.random.geometric(p=.6)):
                params = {
                    'pos' : np.array([random.randint(0, config.MAP_SIZE[0]), random.randint(0, config.MAP_SIZE[1])]),
                    'game_state' : game,
                    'theta' : random.random()*2*np.pi,
                    'speed' : np.array([random.random()*2-1, random.random()*2-1])
                }
                asteroid = np.random.choice([BigAsteroid, MediumAsteroid, SmallAsteroid], p=probabilities)(**params)
                game.add_entity(asteroid)


    @game.on_collide(Asteroid, Asteroid, sym = True)
    def collide(game, ast1, ast2):
        # Fonction de collision entre deux astéroïdes
        # Les astéroïdes vont rebondir l'un sur l'autre

        # On calcule la vitesse relative des deux astéroïdes
        v1 = ast1.speed
        v2 = ast2.speed
        v_rel = v1 - v2

        # On calcule la normale à la collision
        n = ast1.pos - ast2.pos
        n = n / np.linalg.norm(n)

        # On calcule la vitesse de chaque astéroïde dans la direction de la normale
        v1n = np.dot(v1, n)
        v2n = np.dot(v2, n)

        # On calcule la vitesse de chaque astéroïde dans la direction tangentielle
        v1t = v1 - v1n * n
        v2t = v2 - v2n * n

        # On calcule les nouvelles vitesses dans la direction normale
        v1n_new = (v1n * (ast1.mass - ast2.mass) + 2 * ast2.mass * v2n) / (ast1.mass + ast2.mass)
        v2n_new = (v2n * (ast2.mass - ast1.mass) + 2 * ast1.mass * v1n) / (ast1.mass + ast2.mass)

        # On calcule les nouvelles vitesses
        v1_new = v1n_new * n + v1t
        v2_new = v2n_new * n + v2t

        # On applique les nouvelles vitesses
        ast1.speed = v1_new
        ast2.speed = v2_new

        while ast1.intersects(ast2):
            ast1.pos += ast1.speed * config.TICK_TIME
            ast2.pos += ast2.speed * config.TICK_TIME



    game.run()
