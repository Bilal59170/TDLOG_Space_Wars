import pyglet

class Menu:
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

        self.play_button = pyglet.text.Label('Jouer',
                                             font_name='Arial',
                                             font_size=18,
                                             x=self.window.width // 4, y=self.window.height // 2 - 100,
                                             anchor_x='center', anchor_y='center', batch=self.batch)
        
        self.quit_button = pyglet.text.Label('Quitter',
                                             font_name='Arial',
                                             font_size=18,
                                             x=3*(self.window.width // 4), y=self.window.height // 2 - 100,
                                             anchor_x='center', anchor_y='center', batch=self.batch)

    def on_draw(self):
        self.window.clear()
        self.batch.draw()

    def on_mouse_press(self, x, y, button, modifiers):
        if self.play_button.x - self.play_button.content_width // 2 < x < self.play_button.x + self.play_button.content_width // 2 and \
            self.play_button.y - self.play_button.content_height // 2 < y < self.play_button.y + self.play_button.content_height // 2:
            self.window.close()
            self.start_game()

        elif self.quit_button.x - self.quit_button.content_width // 2 < x < self.quit_button.x + self.quit_button.content_width // 2 and \
            self.quit_button.y - self.quit_button.content_height // 2 < y < self.quit_button.y + self.quit_button.content_height // 2:
            self.window.close()