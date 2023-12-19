from asteroids.asteroids import *
import random
import config

def collide(game, ast1, ast2):
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

def activate_collision(game):
    game.on_collide(Asteroid, Asteroid, sym = True)(collide)

def activate_asteroid_spawn(game):
    game.each(5)(spawn_asteroids)



