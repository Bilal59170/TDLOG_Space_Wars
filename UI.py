import pyglet

class Button:
    def __init__(self, x, y, width, height, text, batch):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = pyglet.text.Label(text,
                                      font_name='Arial',
                                      font_size=18,
                                      color=(0, 0, 0, 255),
                                      x=x, y=y,
                                      anchor_x='center', anchor_y='center', batch=batch)
        
        self.rectangle = pyglet.shapes.Rectangle(x - width/2, y - height/2, width, height, color=(255, 255, 255), batch = batch)




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
                                             anchor_x='center', anchor_y='center', batch=self.batch))

        self.play_button = Button(self.window.width // 4, self.window.height // 2 - 100, 100, 50, "Jouer", self.batch)
        self.quit_button = Button(3*(self.window.width // 4), self.window.height // 2 - 100, 100, 50, "Quitter", self.batch)

    def on_draw(self):
        self.window.clear()
        self.batch.draw()


    def on_mouse_press(self, x, y, button, modifiers):
        if self.play_button.on_mouse_press(x, y, button, modifiers):
            self.window.close()
            self.start_game()

        elif self.quit_button.on_mouse_press(x, y, button, modifiers):
            self.window.close()

