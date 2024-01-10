"""
Implémentation de la logique du jeu
Notamment : - Les collisions entre astéroïdes => Fonction activate_collision(game)
            - Le spawn d'astéroïdes           => Fonction activate_asteroid_spawn(game)
"""

import random

import pyglet

import game_engine.config as config
from game_objects.asteroids import *
from game_objects.projectiles import *
from game_objects.ship import Ship
from game_objects.enemies import Enemy
from game_objects.animations import XPLosion

def repel(game, ast, entity):
    """
    Fonction qui repousse les entités des astéroïdes (pour éviter qu'ils ne se chevauchent)
    @params:
        game: la partie
        ast: l'astéroïde
        entity: l'entité à repousser
    """
    
    # On ignore les collisions entre astéroïdes qui sont sur au même endroit
    if ast.pos[0] == entity.pos[0]:
        return

    # On calcule la distance entre l'astéroïde et l'entité
    dist = np.linalg.norm(ast.pos - entity.pos)

    # Si l'entité est trop proche de l'astéroïde, on la repousse
    if dist < ast.size:
        entity.speed += .05 * (ast.pos - entity.pos) * (dist - ast.size) / dist

def collide(game, ast1, ast2):
    """
    Fonction de collision entre deux astéroïdes
    @params:
        game: la partie
        ast1: le premier astéroïde
        ast2: le deuxième astéroïde

    Appelée vua le décorateur on_collide de la classe Game, dans la fonction activate_collision

    Ne pas forcément comprendre le code qui suit, c'est la physique d'un rebond entre deux objets
    Requiert que les astéroïdes aient une masse
    """


    # On ignore les collisions entre astéroïdes qui sont sur au même endroit
    if ast1.pos[0] == ast2.pos[0]:
        return
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



def bullet_asteroid_collision(game, bullet, asteroid):
    asteroid.HP = asteroid.HP - bullet.damage
    if not asteroid.alive:
        if bullet.ship is not None:
            game.player.xp += asteroid.ressources
            XPLosion(bullet.pos, game)

    asteroid.speed += bullet.speed * bullet.mass / asteroid.mass
    game.remove_entity(bullet)

def bullet_enemy_collision(game, bullet, enemy):
    if bullet.ship is not None:
        enemy.HP = enemy.HP - bullet.damage
        if not enemy.alive:
            if bullet.ship is not None:
                game.player.xp += enemy.ressources
                XPLosion(bullet.pos, game)

        #enemy.speed += bullet.speed * bullet.mass / enemy.mass
        game.remove_entity(bullet)

def bullet_ship_collision(game, bullet, ship):
    if bullet.ship is not ship:
        ship.HP = ship.HP - bullet.damage
        game.remove_entity(bullet)


def asteroid_ship_collision(game, asteroid, ship):
    if not(ship.is_invicible):
        ship.HP -= asteroid.damage
        ship.is_invicible = True
    else:
        pass


def spawn_asteroids(game):
    """
    Fonction de spawn d'astéroïdes
    @params:
        game: la partie
    Active le spawn des asétroïdes tous les 5 ticks
    Le nombre d'astéroïdes spawné est aléatoire, et est limité à 20
    """

    # On ne veut pas plus de 20 astéroïdes
    if len(game.asteroids) > 20:
        return

    # On veut que les petits astéroïdes soient plus fréquents que les gros -> on pondère les probabilités
    weights = [10, 20, 50]
    probabilities = [w/sum(weights) for w in weights]

    # On spawn un astéroïde avec une probabilité de 20%
    if random.random() < .2:
        # On choisit un nombre d'astéroïdes à spawn aléatoirement, suivant une loi géométrique de paramètre .6 (1.7 en moyenne)
        for i in range(np.random.geometric(p=.6)):

            # Paramètres de l'astéroïde => position, vitesse, angle, aléatoires
            params = {
                'pos' : np.array([random.randint(0, config.MAP_SIZE[0]), random.randint(0, config.MAP_SIZE[1])]),
                'game_state' : game,
                'theta' : random.random()*2*np.pi,
                'speed' : np.array([random.random()*2-1, random.random()*2-1])
            }

            # On choisit aléatoirement un type d'astéroïde, suivant les probabilités définies plus haut
            asteroid_type = np.random.choice([BigAsteroid, MediumAsteroid, SmallAsteroid], p=probabilities)

            # On vérifie que l'astéroïde ne spawn pas sur un autre
            asteroid = asteroid_type(**params)
            while any([a.intersects(asteroid) for a in game.asteroids]):
                params['pos'] = np.array([random.randint(0, config.MAP_SIZE[0]), random.randint(0, config.MAP_SIZE[1])])
                asteroid = asteroid_type(**params)


            game.add_entity(asteroid)
    

def activate_collision(game):
    """ Active les collisions entre astéroïdes """
    game.on_collide(Asteroid, Asteroid, sym = True)(collide)

    game.on_collide(Projectile, Asteroid)(bullet_asteroid_collision)
    game.on_collide(Projectile, Ship)(bullet_ship_collision)
    game.on_collide(Asteroid, Ship)(asteroid_ship_collision)
    game.on_collide(Projectile, Enemy)(bullet_enemy_collision)

    game.on_collide(Asteroid, Ship)(repel)
    game.on_collide(Asteroid, Enemy)(repel)

def activate_asteroid_spawn(game):
    """ Active le spawn d'astéroïdes """
    game.each(5)(spawn_asteroids)
    game.each(5)(spawn_enemies)



def activate_FPS_counter(game):
    """ Active l'affichage du nombre d'images par seconde """

    game.frame_timer = time.time()
    game.frame_counter = 0 # Compteur de frames
    game.FPS = 0           # FPS
    
    @game.on_draw
    def update_FPS(game):
        pyglet.text.Label('FPS : ' + str(game.FPS),
                            font_name='Times New Roman',
                            font_size=36,
                            color=(255,0,0,255),
                            x=10, y=10).draw()
        
        game.frame_counter += 1
        dt = time.time()-game.frame_timer
        if dt > 1:
            game.FPS =  int(game.frame_counter / dt)
            game.frame_counter = 0
            game.frame_timer = time.time()

    
def spawn_enemies(game):
    """
    Fonction de spawn des ennemis
    @params:
        game: la partie
    Active le spawn des asétroïdes tous les 5 ticks
    Le nombre d'astéroïdes spawné est aléatoire, et est limité à 10
    """

    # On ne veut pas plus de 7 ennemis
    if len(game.enemies) > 5 + game.player.level:
        return

    # On veut que les petits astéroïdes soient plus fréquents que les gros -> on pondère les probabilités
    probabilities = [0.5, 0.30, 0.15, 0.05]
    levels = [0, 1, 2, 3]
    level = np.random.choice(levels, p=probabilities)
    pos = np.array([random.randint(0, config.MAP_SIZE[0]), random.randint(0, config.MAP_SIZE[1])])
    speed = np.array([random.random()*2-1, random.random()*2-1])
    enemy = Enemy(pos, game, speed, level)
    game.add_entity(enemy)
