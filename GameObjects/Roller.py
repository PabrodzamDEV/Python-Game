import pyglet
from typing import Tuple

roller_rows = 1
roller_columns = 10
roller_spritesheet = pyglet.image.load("GameObjects/Assets/roller.png")
# Create image grids and textures for all animations
roller_image_grid = pyglet.image.ImageGrid(roller_spritesheet, roller_rows, roller_columns)
roller_textures = pyglet.image.TextureGrid(roller_image_grid)

roller_initial_speed = -250


class Roller:
    def __init__(self, x, y, batch=None):
        self.roll_animation = pyglet.image.Animation.from_image_sequence(roller_textures[0:], duration=0.1, loop=True)
        self.sprite = pyglet.sprite.Sprite(self.roll_animation, x=x, y=y)
        self.velocity_x = roller_initial_speed

    def update(self, player, border, win_size: Tuple, dt):
        # Update position based on velocity
        self.sprite.x += self.velocity_x * dt
        if not player.is_running and player.velocity_x > 0:
            self.velocity_x = roller_initial_speed + roller_initial_speed // 2
        elif not player.is_running and player.velocity_x < 0:
            self.velocity_x = roller_initial_speed - player.velocity_x * 50
        elif player.is_running and player.velocity_x > 0:
            self.velocity_x = roller_initial_speed * 2
        elif player.is_running and player.velocity_x < 0:
            self.velocity_x = roller_initial_speed // 3
        else:
            self.velocity_x = roller_initial_speed
        if self.sprite.x <= border:
            self.sprite.x = win_size[0]

    def draw(self):
        self.sprite.draw()
