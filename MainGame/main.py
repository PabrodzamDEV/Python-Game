import time
import random
import sqlite3
import pyglet
from GameObjects import Load

# Constants that define game parameters
WIDTH = 1200
BORDER = 30
player_posx = WIDTH // 3
player_posy = BORDER
SCORE_LABEL_X = BORDER
SCORE_LABEL_Y = BORDER
background_image = pyglet.image.load("Resources/desert_background_720.png")
HEIGHT = background_image.height
# This determines the number of backgrounds that will be drawn in order to achieve
# the infinite background effect. 3 pretty much guarantees it
tiles = (WIDTH // background_image.width) * 3
# Load background music
bg_music = pyglet.media.load('Resources/desert_music.mp3', streaming=False)
bg_music_player = pyglet.media.Player()
bg_music_player.queue(bg_music)
bg_music_player.loop = True
# Load custom font for labels
custom_font_path = 'Resources/PressStart2P.ttf'
pyglet.font.add_file(custom_font_path)

# Create a connection to an SQLite database (or create a new one if it doesn't exist)
conn = sqlite3.connect('scores.db')

# Create a cursor object to interact with the database
cursor = conn.cursor()

# Create a table to store the scores if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS scores (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        score INTEGER
    )
''')

# Commit the changes
conn.commit()

# Retrieve the highest score from the database
cursor.execute('SELECT MAX(score) FROM scores')
highest_score = cursor.fetchone()[0]

# Close the connection
conn.close()

"""
Decorator function that measures the distance the player has travelled in the (positive) x axis.

Args:
    function (function): The function to be decorated.

Returns:
    function: The wrapper function that measures the player distance.
"""


def measure_player_distance(function):
    def wrapper(self, dt):
        func = function(self, dt)
        if self.player.velocity_x > 0:
            self.player_distance += self.player.velocity_x

        return func

    return wrapper


# Class which represents an infinite background
class InfiniteBackground(pyglet.sprite.Sprite):
    def __init__(self, image, x, y, batch=None):
        super(InfiniteBackground, self).__init__(image, x=x, y=y, batch=batch)
        self.width, self.height = image.width, image.height
        bg_music_player.play()

    def update(self, player_velocity_x, dt):
        # Update background position based on player movement
        self.x -= (player_velocity_x * 80) * dt

        # Check if the background has moved entirely off-screen, and reset its position
        if self.x + self.width <= 0:
            # Move the 'right-most' background to the right of the last background
            self.x += self.width * tiles
        if self.x >= WIDTH:
            # Move the 'left-most' background to the left of the last background
            self.x -= self.width * tiles


class MajueloSouls(pyglet.window.Window):
    def __init__(self):
        super(MajueloSouls, self).__init__(WIDTH, HEIGHT, "MajueloSouls", resizable=False)
        self.highest_score = 0  # Make sure it is set at least to 0
        # If there is a highest score in the database, use it
        if highest_score is not None:
            self.highest_score = highest_score
        self.main_batch = pyglet.graphics.Batch()
        self.win_size = (WIDTH, HEIGHT)
        # Create a label to show controls
        self.controls_label = pyglet.text.Label('MOVE [A] [D]\n\nJUMP [SPACE]\n\nATTACK [K]\n\nSPRINT [L]'
                                                '\n\nEXIT [ESC]\n\nRESTART [C]',
                                                font_name='Press Start 2P',
                                                font_size=12,
                                                x=BORDER + WIDTH // 3.5, y=HEIGHT - BORDER * 5,
                                                multiline=True,
                                                width=WIDTH // 2,
                                                anchor_x='center', anchor_y='center',
                                                color=(255, 255, 255, 255))

        # Create a label for the score
        self.score_label = pyglet.text.Label('SCORE: ',
                                             font_name='Press Start 2P',
                                             font_size=12,
                                             x=WIDTH // 2, y=HEIGHT - BORDER * 2,
                                             anchor_x='center', anchor_y='center',
                                             color=(0, 255, 0, 255))

        # Create a label for the score
        self.higher_score_label = pyglet.text.Label('RECORD: ',
                                                    font_name='Press Start 2P',
                                                    font_size=12,
                                                    x=WIDTH // 2, y=HEIGHT - BORDER * 4,
                                                    anchor_x='center', anchor_y='center',
                                                    color=(0, 255, 0, 255))

        # Create a label for when the game is over
        self.game_over_label = pyglet.text.Label('GAME OVER',
                                                 font_name='Press Start 2P',
                                                 font_size=36,
                                                 x=WIDTH // 2, y=HEIGHT // 2,
                                                 anchor_x='center', anchor_y='center',
                                                 color=(255, 0, 0, 255))

        # Create multiple instances of the background
        self.backgrounds = [
            InfiniteBackground(background_image, x=i * background_image.width, y=0, batch=self.main_batch)
            for i in range(tiles)  # Adjust the number of backgrounds based on the window's needs
        ]

        # Create game walls
        self.walls = Load.load_walls(self.win_size, BORDER, batch=self.main_batch)

        # Create a player instance
        self.player = Load.load_player(((WIDTH - BORDER) // 2), player_posy, batch=self.main_batch)
        self.player_distance = 0

        # Create a list to store active enemy instances
        self.max_enemies = 1
        self.possible_enemy_y_positions = [BORDER, 50, 70, 90, 110, 130]
        self.possible_enemy_x_positions = [WIDTH - BORDER - 70, WIDTH - BORDER - 60, WIDTH - BORDER - 50,
                                           WIDTH - BORDER - 40, WIDTH - BORDER - 30, WIDTH - BORDER - 20]
        self.active_enemies = []
        self.last_enemy_spawn_time = time.time()
        self.start_enemy_appending()
        self.roller = Load.load_roller(WIDTH - BORDER - 120, BORDER, batch=self.main_batch)
        # Set event handlers
        self.push_handlers(self.player)
        # Wait for an amount of seconds before generating the next enemy
        self.start_enemy_appending()

    def on_key_press(self, symbol, modifiers):
        # Check if the pressed key is left or right arrow
        if symbol == pyglet.window.key.ESCAPE:
            self.close()
        elif symbol == pyglet.window.key.C:
            self.restart_game()

    def restart_game(self):
        self.player = Load.load_player(((WIDTH - BORDER) // 2), player_posy, batch=self.main_batch)
        # Set event handlers
        self.push_handlers(self.player)
        self.roller = Load.load_roller(WIDTH - BORDER - 120, BORDER, batch=self.main_batch)
        self.active_enemies.clear()
        self.player_distance = 0

    def generate_enemies(self):
        random_y_position = random.choice(self.possible_enemy_y_positions)
        random_x_position = random.choice(self.possible_enemy_x_positions)
        yield Load.load_enemy(random_x_position, random_y_position, batch=self.main_batch)

    def append_enemy(self):
        # Append an enemy if the time difference is greater than 1 second
        current_time = time.time()
        if current_time - self.last_enemy_spawn_time >= 1 and len(self.active_enemies) < self.max_enemies:
            self.active_enemies.append(next(self.generate_enemies()))
            self.last_enemy_spawn_time = current_time

    def start_enemy_appending(self):
        pyglet.clock.schedule_interval(lambda dt: self.append_enemy(), 1 / 60.0)

    def on_draw(self):
        self.clear()
        self.main_batch.draw()
        self.player.draw()
        # Draw each active enemy in the list
        for enemy in self.active_enemies:
            enemy.draw()
        self.roller.draw()
        self.controls_label.draw()
        # Update the text of the score_label with the current player_distance
        self.score_label.text = 'SCORE: {}'.format(int(self.player_distance))
        self.score_label.draw()

        if self.highest_score > 0:
            self.higher_score_label.text = 'RECORD: {}'.format(int(self.highest_score))
        self.higher_score_label.draw()
        if self.player.is_dying:
            # Insert the player's score into the database when the player dies
            conn = sqlite3.connect('scores.db')
            cursor = conn.cursor()
            # Insert a new record, if that is the case
            if self.player_distance > self.highest_score:
                cursor.execute('INSERT INTO scores (score) VALUES (?)', (int(self.player_distance),))
                self.highest_score = self.player_distance
            conn.commit()
            conn.close()
            self.game_over_label.draw()

    @measure_player_distance
    def update(self, dt):
        # Update the player
        self.player.update(BORDER, self.win_size, dt, self.active_enemies, self.roller)
        if self.player.current_animation == self.player.jump_animation:
            self.player.keys[pyglet.window.key.K] = False

            # Update all active enemies in the list
        for enemy in self.active_enemies:
            enemy.update(self.player, BORDER, self.win_size, dt)
            if enemy.exited_screen:
                self.active_enemies.remove(enemy)
        # update roller instance
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
    game.set_location(350, 50)
    game.run()
