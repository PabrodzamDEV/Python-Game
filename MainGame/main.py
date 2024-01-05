import time
import random

import pyglet
from GameObjects import Load

# Constants that define game parameters
WIDTH = 1200
BORDER = 30
player_posx = WIDTH // 3
player_posy = BORDER
SCORE_LABEL_X = BORDER
SCORE_LABEL_Y = BORDER
background_image = pyglet.image.load("Resources/desert_background.png")
HEIGHT = background_image.height
tiles = (WIDTH // background_image.width) * 2


class InfiniteBackground(pyglet.sprite.Sprite):
    def __init__(self, image, x, y, batch=None):
        super(InfiniteBackground, self).__init__(image, x=x, y=y, batch=batch)
        self.width, self.height = image.width, image.height

    def update(self, player_velocity_x, dt):
        # Update background position based on player movement
        self.x -= (player_velocity_x * 80) * dt

        # Check if the background has moved entirely off-screen, and reset its position
        if self.x + self.width <= 0:
            # Move the background to the right of the last background
            self.x += self.width * tiles
        if self.x >= WIDTH:
            # Move the background to the right of the last background
            self.x -= self.width * tiles


class MajueloSouls(pyglet.window.Window):
    def __init__(self):
        super(MajueloSouls, self).__init__(WIDTH, HEIGHT)
        self.main_batch = pyglet.graphics.Batch()
        self.win_size = (WIDTH, HEIGHT)

        # Create multiple instances of the background
        self.backgrounds = [
            InfiniteBackground(background_image, x=i * background_image.width, y=0, batch=self.main_batch)
            for i in range(tiles)  # Adjust the number of backgrounds based on the window's needs
        ]

        # Create game walls
        self.walls = Load.load_walls(self.win_size, BORDER, batch=self.main_batch)

        # Create a player instance
        self.player = Load.load_player(((WIDTH - BORDER) // 2), player_posy, batch=self.main_batch)

        # Create a list to store active enemy instances
        self.max_enemies = 5
        self.possible_enemy_y_positions = [BORDER, 50, 70, 90, 110, 130]
        self.possible_enemy_x_positions = [WIDTH - BORDER - 70, WIDTH - BORDER - 60, WIDTH - BORDER - 50,
                                           WIDTH - BORDER - 40, WIDTH - BORDER - 30, WIDTH - BORDER - 20]
        self.active_enemies = []
        self.last_enemy_spawn_time = time.time()
        self.start_enemy_appending()
        self.roller = Load.load_roller(WIDTH - BORDER - 120, BORDER, batch=self.main_batch)
        # Set event handlers
        self.push_handlers(self.player)

    def generate_enemies(self):
        random_y_position = random.choice(self.possible_enemy_y_positions)
        random_x_position = random.choice(self.possible_enemy_x_positions)
        yield Load.load_enemy(random_x_position, random_y_position, batch=self.main_batch)

    def append_enemy(self):
        # Append an enemy if the time difference is greater than 2 seconds
        current_time = time.time()
        if current_time - self.last_enemy_spawn_time >= 5.0 and len(self.active_enemies) < self.max_enemies:
            self.active_enemies.append(next(self.generate_enemies()))
            self.last_enemy_spawn_time = current_time

    def start_enemy_appending(self):
        pyglet.clock.schedule_interval(lambda dt: self.append_enemy(), 1 / 60.0)

    def on_draw(self):
        self.clear()
        self.main_batch.draw()
        self.player.draw()
        # Wait for an amount of seconds before generating the next enemy
        self.start_enemy_appending()
        # Draw each active enemy in the list
        for enemy in self.active_enemies:
            enemy.draw()
        self.roller.draw()

    def update(self, dt):
        # Update the player
        self.player.update(BORDER, self.win_size, dt)
        if self.player.current_animation == self.player.jump_animation:
            self.player.keys[pyglet.window.key.K] = False

            # Update all active enemies in the list
        for enemy in self.active_enemies:
            enemy.update(self.player, BORDER, self.win_size, dt)
        self.roller.update(self.player, BORDER, self.win_size, dt)
        # Update all background instances
        for background in self.backgrounds:
            background.update(self.player.velocity_x, dt)

    def run(self):
        # Schedule the update function
        pyglet.clock.schedule_interval(self.update, 1 / 60.0)
        # Run the application
        pyglet.app.run()


# Instantiate and run the game
if __name__ == "__main__":
    game = MajueloSouls()
    game.run()
