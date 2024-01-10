import pyglet

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


        self.labels.append(pyglet.text.Label('New Diep.io',
                                             font_name='Arial',
                                             font_size=24,
                                             x=self.window.width // 2, y=self.window.height // 2,
                                             anchor_x='center', anchor_y='center'))

        self.play_button = Button(self.window.width // 4, self.window.height // 2 - 100, 100, 50, "Jouer")
        self.quit_button = Button(3*(self.window.width // 4), self.window.height // 2 - 100, 100, 50, "Quitter")

    def on_draw(self):
        self.window.clear()
        self.labels[0].draw()
        self.play_button.draw()
        self.quit_button.draw()


    def on_mouse_press(self, x, y, button, modifiers):
        if self.play_button.on_mouse_press(x, y, button, modifiers):
            self.window.close()
            self.start_game()

        elif self.quit_button.on_mouse_press(x, y, button, modifiers):
            self.window.close()





class DeathMenu:
    def __init__(self, window):
        self.window = window
        self.batch = pyglet.graphics.Batch()
        self.labels = []

        self.window.on_draw = self.on_draw

        self.window.on_mouse_press = self.on_mouse_press
        
        self.labels.append(pyglet.text.Label('Game Over',
                                             font_name='Arial',
                                             font_size=24,
                                             x=self.window.width // 2, y=self.window.height // 2,
                                             anchor_x='center', anchor_y='center'))

        self.play_button = Button(self.window.width // 4, self.window.height // 2 - 100, 100, 50, "Rejouer")
        self.quit_button = Button(3*(self.window.width // 4), self.window.height // 2 - 100, 100, 50, "Quitter")

    def on_draw(self):
        #self.window.clear()
        self.play_button.draw()
        self.quit_button.draw()
        


    def on_mouse_press(self, x, y, button, modifiers):
        if self.play_button.on_mouse_press(x, y, button, modifiers):
            self.window.close()
            self.game.restart()

        elif self.quit_button.on_mouse_press(x, y, button, modifiers):
            self.window.close()
            self.game.close()