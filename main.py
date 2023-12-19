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

import game_logic

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



#     game.run()


""" LES TESTS DE BIL """


img_caca = pyglet.image.load("Sprites/caca.png")

if __name__ == "__main__":

    game = Game()

    spacing = 50

    asteroid = MasterAsteroid([spacing, 0], game)             # Position (0, 0) sur la carte => Au milieu de l'écran quand le vaisseau est en (0, 0) !
    game.add_entity(asteroid)
    asteroid = BigAsteroid([MAP_SIZE[0]-spacing, 0], game)
    game.add_entity(asteroid)
    asteroid = SmallAsteroid([0, MAP_SIZE[1]-spacing], game)
    game.add_entity(asteroid)
    asteroid = MediumAsteroid([MAP_SIZE[0]-spacing, MAP_SIZE[1]-spacing], game)
    game.add_entity(asteroid)

    n = 5
    for x in range(0, MAP_SIZE[0], MAP_SIZE[0] // n):
        for y in range(0, MAP_SIZE[1], MAP_SIZE[1] // n):
            text = sprites.Label([x, y], f"{x}, {y}", game, color=(0,0,0,255))
            game.add_entity(text)




    # Deux cacas. Le deuxième va plus vite et est incliné (normalement) (ne fonctionne pas !)
    caca = sprites.Image(np.array([-500, 0]), img_caca, game)
    caca2 = sprites.Image(np.array([500, 0]), img_caca, game, speed=[-10, 0], theta=np.pi/6)

    game.add_entity(caca)
    game.add_entity(caca2)

    # Animation de l'ogre !
    images = [pyglet.image.load(f'Sprites/animation/an_{i}.png') for i in range(1, 6)]
    animation = pyglet.image.Animation.from_image_sequence(images, .5)
    img = sprites.Image(np.array([0, 0]), animation, game)
    game.add_entity(img)



    # Game Logic => Collision et spawn d'astéroïdes
    game_logic.activate_collision(game)
    # game_logic.activate_asteroid_spawn(game)

    game.run()
