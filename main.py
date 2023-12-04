import pyglet
from pyglet.window import key, mouse
from ship import Ship
import numpy as np
import game
import config

# from game import *

"""@package docstring
Fichier d'application (sert pour l'instant à tester le code produit)


"""

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


# Create a window
window = pyglet.window.Window()
game_test = game.Game()

if __name__ ==  '__main__':
    #initialisation  du vaisseau test


    @window.event
    def on_draw():
        # Clear the window
        window.clear()
        game_test.player.draw()

    
    # Start the main event loop (+define the tick duration in seconds for update functions)
    pyglet.clock.schedule_interval(game_test.update, config.TICK_TIME)
    pyglet.app.run()



# music = pyglet.resource.media("ost/bgm_forever.mp3")
# music.play()

# @window.event
# def on_mouse_press(x, y, button, modifiers):
#     if button == mouse.LEFT:
#         # Ship.shoot()
#         print("The left mouse button was pressed.")


# @window.event
# def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
#     # Modify ship orientation
#     print(f"Mouse moved. Current coordinates : {x}, {y}")




@window.event
def on_draw():
    # Clear the window
    window.clear()

    # Create a batch to hold our graphics
    # batch = pyglet.graphics.Batch()

    # Draw a red rectangle
    # x, y, width, height = 100, 100, 200, 150
    # radius = 25
    # pyglet.shapes.Circle(x, y, radius, color=(255, 0, 0), batch=batch).draw()

    # Create the ship
    # current_game = Game()
    ship_test = Ship(np.array([100, 100]), np.array([0, 0]), 50)
    ship_test.draw()


# Start the main event loop (+define the tick duration in seconds for update functions)
# pyglet.clock.schedule_interval(update, TICK_TIME)
pyglet.app.run()

