import pyglet
from typing import Tuple

# Load enemy spritesheets
appear_spritesheet = pyglet.image.load("GameObjects/Assets/ghost_appear.png")
idle_spritesheet = pyglet.image.load("GameObjects/Assets/ghost_idle.png")
vanish_spritesheet = pyglet.image.load("GameObjects/Assets/ghost_vanish.png")

# Load enemy sound
vanish_sound = pyglet.media.load('Resources/enemy_vanish.wav', streaming=False)

# Calculate frame size for appear animation
appear_rows = 1
appear_columns = 6

# Calculate frame size for idle animation
idle_rows = 1
idle_columns = 7

# Calculate frame size for vanish animation
vanish_rows = 1
vanish_columns = 7

# Create image grids and textures for all animations
appear_image_grid = pyglet.image.ImageGrid(appear_spritesheet, appear_rows, appear_columns)
appear_textures = pyglet.image.TextureGrid(appear_image_grid)

idle_image_grid = pyglet.image.ImageGrid(idle_spritesheet, idle_rows, idle_columns)
idle_textures = pyglet.image.TextureGrid(idle_image_grid)

vanish_image_grid = pyglet.image.ImageGrid(vanish_spritesheet, vanish_rows, vanish_columns)
vanish_textures = pyglet.image.TextureGrid(vanish_image_grid)

enemy_initial_speed = -150


class Enemy:
    def __init__(self, x, y, batch=None):
        self.appear_animation = pyglet.image.Animation.from_image_sequence(appear_textures[0:],
                                                                           duration=0.1, loop=False)
        self.idle_animation = pyglet.image.Animation.from_image_sequence(idle_textures[0:],
                                                                         duration=0.1, loop=True)
        self.vanish_animation = pyglet.image.Animation.from_image_sequence(vanish_textures[0:],
                                                                           duration=0.1, loop=True)
        self.current_animation = self.appear_animation
        self.sprite = pyglet.sprite.Sprite(self.appear_animation, x=x, y=y)
        self.velocity_x = enemy_initial_speed
        pyglet.clock.schedule_once(self.appear_animation_complete, self.appear_animation.get_duration())
        self.hit = False
        self.exited_screen = False
        # Flag to check if the vanish sound has been played
        self.vanish_sound_played = False

    def appear_animation_complete(self, dt):
        self.current_animation = self.idle_animation
        self.sprite.image = self.idle_animation

    def update(self, player, border, win_size: Tuple, dt):
        self.sprite.x += self.velocity_x * dt
        if not player.is_running and player.velocity_x > 0:
            self.velocity_x = (enemy_initial_speed - player.velocity_x) * 2
        elif not player.is_running and player.velocity_x < 0:
            self.velocity_x = enemy_initial_speed - enemy_initial_speed // 2
        elif player.is_running and player.velocity_x > 0:
            self.velocity_x = (enemy_initial_speed - player.velocity_x) * 3
        elif player.is_running and player.velocity_x < 0:
            self.velocity_x = 1
        else:
            self.velocity_x = enemy_initial_speed

        if (((
                (player.current_animation == player.attack_animation
                 or player.current_animation == player.attack_left_animation
                 or player.current_animation == player.air_attack_animation
                 or player.current_animation == player.air_attack_left_animation)
                and (player.sprite.x + player.player_width) >= self.sprite.x)
                and not (player.sprite.x + player.player_width / 2.3) >= self.sprite.x
                and (player.sprite.y + player.sprite.height / 5) >= self.sprite.y)
                and not (player.sprite.y + player.sprite.height / 5) > (self.sprite.y + self.sprite.height)):
            self.hit = True
            if not self.vanish_sound_played:
                vanish_sound.play()
                self.vanish_sound_played = True
            self.current_animation = self.vanish_animation
            self.sprite.image = self.vanish_animation

        if self.sprite.x <= border:
            self.exited_screen = True

    def draw(self):
        self.sprite.draw()
