import pyglet
from game_engine.utils import *

class Button:
    def __init__(self, x, y, width, height, text):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rectangle = pyglet.shapes.Rectangle(x - width/2, y - height/2, width, height, color=(255, 255, 255))
        self.text = pyglet.text.Label(text,
                                      font_name='Arial',
                                      font_size=18,
                                      color=(0, 0, 0, 255),
                                      x=x, y=y,
                                      anchor_x='center', anchor_y='center')
        
    def draw(self) :
        self.rectangle.draw()
        self.text.draw()
        




    def on_mouse_press(self, x, y, button, modifiers):
        if self.x - self.width // 2 < x < self.x + self.width // 2 and \
            self.y - self.height // 2 < y < self.y + self.height // 2:
            return True
        return False

# Exactement la même classe mais qui utilise la classe button
class StartMenu:
    def __init__(self):
        self.window = pyglet.window.Window(width=800, height=600, caption="Game Menu")
        self.batch = pyglet.graphics.Batch()
        self.labels = []

        self.window.on_draw = self.on_draw

        self.window.on_mouse_press = self.on_mouse_press
        
        Y_LABEL = 200

        self.labels.append(pyglet.text.Label('New Diep.io',
                                             font_name='Arial',
                                             font_size=24,
                                             x=self.window.width // 2, y=Y_LABEL,
                                             anchor_x='center', anchor_y='center'))

        self.play_button = Button(self.window.width // 4, Y_LABEL - 100, 100, 50, "Jouer")
        self.quit_button = Button(3*(self.window.width // 4), Y_LABEL - 100, 100, 50, "Quitter")
        self.make_grid()

    def on_draw(self):
        self.window.clear()
        self.labels[0].draw()
        self.play_button.draw()
        self.quit_button.draw()
        self.text.draw()


    def on_mouse_press(self, x, y, button, modifiers):
        if self.play_button.on_mouse_press(x, y, button, modifiers):
            self.window.close()
            self.start_game()

        elif self.quit_button.on_mouse_press(x, y, button, modifiers):
            self.window.close()

    def make_grid(self):
        scores = read_scoreboard()
        lines = []
        for score, player in scores:
            lines += [f"{player:.<20} : {score}"]

        print('\n'.join(lines))
        
        document = pyglet.text.document.FormattedDocument('\n'.join(lines))
        document.set_style(0,len(document.text),dict(color=(255,255,255,255), font_size=21, font_name="Consolas"))
        self.text = pyglet.text.layout.ScrollableTextLayout(document,int(self.window.width / 1.7),420, multiline=True)
        self.text.x = self.window.width // 4
        self.text.y=self.window.height-100
        self.text.anchor_y="top"
