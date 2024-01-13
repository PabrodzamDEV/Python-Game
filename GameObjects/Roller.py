import pyglet
from typing import Tuple

# Load sprite sheet for the roller
roller_spritesheet = pyglet.image.load("GameObjects/Assets/roller.png")

# Set the number of rows and columns in the sprite sheet
roller_rows = 1
roller_columns = 10

# Create image grids and textures for all animations
roller_image_grid = pyglet.image.ImageGrid(roller_spritesheet, roller_rows, roller_columns)
roller_textures = pyglet.image.TextureGrid(roller_image_grid)

# Set base speed for the roller
roller_base_speed = -350


class Roller:
    def __init__(self, x, y, batch=None):
        self.idle_animation = pyglet.image.Animation.from_image_sequence(roller_textures[0:], duration=0.1, loop=True)
        self.current_animation = self.idle_animation
        self.sprite = pyglet.sprite.Sprite(self.idle_animation, x=x, y=y)
        self.velocity_x = roller_base_speed

    def update(self, player, border, win_size: Tuple, dt):
        # Update position based on velocity
        self.sprite.x += self.velocity_x * dt
        # If the player is moving, speed changes to create the effect that
        # the player is actually moving closer or further away from the roller
        if not player.is_running and player.velocity_x > 0:
            self.velocity_x = roller_base_speed + roller_base_speed / 2
        elif not player.is_running and player.velocity_x < 0:
            self.velocity_x = roller_base_speed - player.velocity_x * 50
        elif player.is_running and player.velocity_x > 0:
            self.velocity_x = roller_base_speed * 2.2
        elif player.is_running and player.velocity_x < 0:
            self.velocity_x = roller_base_speed / 3
        else:
            self.velocity_x = roller_base_speed
        if self.sprite.x <= border:
            self.sprite.x = win_size[0]

    def draw(self):
        self.sprite.draw()
