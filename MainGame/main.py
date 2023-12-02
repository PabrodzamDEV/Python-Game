import pyglet
from GameObjects.Player import Player

# Constantes que marcarán parámetros del juego
WIDTH = 1200
HEIGHT = 900
SCORE_LABEL_X = WIDTH // 2
SCORE_LABEL_Y = HEIGHT // 2


class MajueloSouls(pyglet.window.Window):
    def __init__(self):
        super(MajueloSouls, self).__init__(WIDTH, HEIGHT)

        # Create a Knight instance
        self.player = Player(x=WIDTH // 2, y=HEIGHT // 2)

        # Set event handlers
        self.push_handlers(self.player)

    def on_draw(self):
        self.clear()
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
