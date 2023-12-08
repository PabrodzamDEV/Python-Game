import pyglet

from GameObjects import Load
from GameObjects.Player import Player

# Constantes que marcarán parámetros del juego
WIDTH = 800
HEIGHT = 600
BORDER = 30
SCORE_LABEL_X = WIDTH // 2
SCORE_LABEL_Y = HEIGHT // 2


class MajueloSouls(pyglet.window.Window):
    def __init__(self):
        super(MajueloSouls, self).__init__(WIDTH, HEIGHT)
        self.main_batch = pyglet.graphics.Batch()
        self.win_size = (WIDTH, HEIGHT)
        # Create game walls
        self.walls = Load.load_walls(self.win_size, BORDER, batch=self.main_batch)

        # Create a Knight instance
        self.player = Player(x=(WIDTH // 3), y=BORDER)

        # Set event handlers
        self.push_handlers(self.player)

    def on_draw(self):
        self.clear()
        self.main_batch.draw()
        self.player.draw()

    def update(self, dt):
        # Update the Knight
        self.player.update(dt)

    def run(self):
        # Schedule the update function
        pyglet.clock.schedule_interval(self.update, 1 / 60.0)
        # Run the application
        pyglet.app.run()


# Instantiate and run the game
if __name__ == "__main__":
    game = MajueloSouls()
    game.run()
