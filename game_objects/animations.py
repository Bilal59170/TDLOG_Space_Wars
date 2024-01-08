import sys
sys.path.append("../")

from game_engine import sprites
import pyglet


class Animation(sprites.Image):
    """ Classe Animation à utiliser pour les animations de sprites à durée de vie limitée """

    def __init__(self, pos, game_state, theta=None, speed=[0,0], use_mask=True, rotates_often=False):

        if hasattr(self, "animation"):
            animation = self.animation
        else:
            raise NotImplementedError("You must define a class attribute 'animation' in your Animation subclass.")

        super().__init__(pos, animation, game_state, theta, speed, use_mask, rotates_often)
        game_state.add_entity(self)

    def tick(self):
        super().tick()
        if self.animation_time >= self.animation_duration:
            self.game_state.remove_entity(self)


images = [pyglet.image.load(f'resources/Sprites/xplosion/xplosion-{i}.png') for i in range(0, 17)]
for im in images:
    # set the anchor so that it is centered
    im.anchor_x = im.width // 2
    im.anchor_y = im.height // 2

animation = pyglet.image.Animation.from_image_sequence(images, .1)

class XPLosion(Animation):
    animation = animation