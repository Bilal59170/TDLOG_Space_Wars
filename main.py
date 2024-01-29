"""! @brief Fichier de lancement du jeu.

@mainpage diep.io

@section description_main Description
Un programme qui permet de lancer le jeu diep.io, avec un menu de démarrage.
"""



from game import Game
# gestion du jeu
import game_logic

import pyglet
from UI import StartMenu

def start_game(player_name):
    """! @brief Fonction qui lance le jeu après le menu de démarrage 
    @param player_name Nom du joueur
    """

    # On crée le jeu
    game = Game(profile=False)

    # On active les différentes fonctionnalités
    game_logic.activate_collision(game)
    game_logic.activate_asteroid_spawn(game)
    game_logic.activate_FPS_counter(game)

    # On lance le jeu
    game.player_name = player_name
    game.run()

if __name__ == "__main__":
    # On lance le menu de démarrage
    menu = StartMenu()
    menu.start_game = start_game
    pyglet.app.run()

