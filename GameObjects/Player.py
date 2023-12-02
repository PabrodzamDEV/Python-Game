import pyglet
import os

from pyglet.window import key


class Player:
    def __init__(self, x, y, speed=200):
        # Load sprite sheets for run and idle animations
        # Get the current script's directory
        # Set the knight's speed
        self.speed = speed
        self.jump_speed = 300
        self.is_jumping = False
        self.gravity = 1000
        self.initial_y = y
        self.is_running = False
        self.keys = {pyglet.window.key.D: False, pyglet.window.key.A: False,
                     pyglet.window.key.MOD_SHIFT: False, pyglet.window.key.SPACE: False}
        # Initialize velocity
        self.velocity_x = 0
        self.velocity_y = 0
        current_directory = os.path.dirname(os.path.abspath(__file__))
        # Define the relative path to the sprite sheets
        run_spritesheet_path = os.path.join(current_directory, "Assets", "assassin_run_right.png")
        run_left_spritesheet_path = os.path.join(current_directory, "Assets", "assassin_run_left.png")
        idle_spritesheet_path = os.path.join(current_directory, "Assets", "assassin_idle.png")
        junp_spritesheet_path = os.path.join(current_directory, "Assets", "assassin_jump.png")

        run_right_spritesheet = pyglet.image.load(run_spritesheet_path)
        run_left_spritesheet = pyglet.image.load(run_left_spritesheet_path)
        idle_spritesheet = pyglet.image.load(idle_spritesheet_path)
        jump_spritesheet = pyglet.image.load(junp_spritesheet_path)

        # Calculate frame size for run animation
        run_rows = 1
        run_columns = 8
        run_frame_width = run_right_spritesheet.width // run_columns
        run_frame_height = run_right_spritesheet.height // run_rows

        # Calculate frame size for idle animation
        idle_rows = 1
        idle_columns = 8
        idle_frame_width = idle_spritesheet.width // idle_columns
        idle_frame_height = idle_spritesheet.height // idle_rows

        # Calculate frame size for jump animation
        jump_rows = 1
        jump_columns = 3
        jump_frame_width = jump_spritesheet.width // jump_columns
        jump_frame_height = jump_spritesheet.height // jump_rows

        # Create image grids and textures for run animation
        run_image_grid = pyglet.image.ImageGrid(run_right_spritesheet, run_rows, run_columns)
        run_textures = pyglet.image.TextureGrid(run_image_grid)
        run_left_image_grid = pyglet.image.ImageGrid(run_left_spritesheet, run_rows, run_columns)
        run_left_textures = pyglet.image.TextureGrid(run_left_image_grid)

        # Create image grids and textures for idle animation
        idle_image_grid = pyglet.image.ImageGrid(idle_spritesheet, idle_rows, idle_columns)
        idle_textures = pyglet.image.TextureGrid(idle_image_grid)

        # Create image grids and textures for jump animation
        jump_image_grid = pyglet.image.ImageGrid(jump_spritesheet, jump_rows, jump_columns)
        jump_textures = pyglet.image.TextureGrid(jump_image_grid)

        # Create run animation
        self.run_animation = pyglet.image.Animation.from_image_sequence(run_textures[0:], duration=0.1, loop=True)
        self.run_left_animation = pyglet.image.Animation.from_image_sequence(run_left_textures[0:], duration=0.1,
                                                                             loop=True)

        # Create idle animation
        self.idle_animation = pyglet.image.Animation.from_image_sequence(idle_textures[0:], duration=0.1, loop=True)

        # Create jump animation
        self.jump_animation = pyglet.image.Animation.from_image_sequence(jump_textures[0:], duration=0.1, loop=True)

        # Set initial animation to idle
        self.current_animation = self.idle_animation

        # Create sprite
        self.sprite = pyglet.sprite.Sprite(self.current_animation, x=x, y=y)

    def update(self, dt):
        # Update animations or other logic here
        # Update position based on velocity
        self.sprite.x += self.velocity_x * dt
         # self.velocity_y -= self.gravity * dt
        # Check if the player is jumping
        if self.is_jumping:
            # Update the jump behavior
            self.sprite.y += self.velocity_y * dt
            self.update_jump(dt)
            self.velocity_y -= self.gravity * dt

    def on_key_press(self, symbol, modifiers):
        # Check if the pressed key is left or right arrow
        if symbol == pyglet.window.key.D:
            self.keys[symbol] = True
            self.velocity_x = self.speed
            self.current_animation = self.run_animation
            self.sprite.image = self.run_animation
        elif symbol == pyglet.window.key.A:
            self.keys[symbol] = True
            self.velocity_x = -self.speed
            self.current_animation = self.run_left_animation
            self.sprite.image = self.run_left_animation
        elif symbol == pyglet.window.key.SPACE:
            self.keys[symbol] = True
            self.jump()
        elif modifiers & key.MOD_SHIFT:
            self.keys[key.MOD_SHIFT] = True
        if self.keys[key.MOD_SHIFT] and not self.is_running:
            self.is_running = True
            self.velocity_x *= 2

    def on_key_release(self, symbol, modifiers):
        # Check if the released key is left or right arrow
        if symbol in (pyglet.window.key.D, pyglet.window.key.A):
            self.keys[symbol] = False
            self.velocity_x = 0
            self.current_animation = self.idle_animation
            self.sprite.image = self.idle_animation
        elif symbol == pyglet.window.key.SPACE:
            self.keys[symbol] = False
            self.velocity_y = 0
            if self.keys[pyglet.window.key.D]:
                self.current_animation = self.run_animation
                self.sprite.image = self.run_animation
            elif self.keys[pyglet.window.key.A]:
                self.current_animation = self.run_left_animation
                self.sprite.image = self.run_left_animation
            else:
                self.current_animation = self.idle_animation
                self.sprite.image = self.idle_animation
        elif modifiers or key.MOD_SHIFT:
            self.keys[key.MOD_SHIFT] = False
            self.is_running = False
            self.velocity_x /= 2

    def jump(self):
        if not self.is_jumping:
            self.velocity_y = self.jump_speed
            self.is_jumping = True
            self.current_animation = self.jump_animation
            self.sprite.image = self.jump_animation

    def update_jump(self, dt):
        # Check if the player has ascended above or descended below the initial y position
        if self.sprite.y < self.initial_y:
            # If descending below, reset to initial y position and stop the jump
            self.sprite.y = self.initial_y
            self.velocity_y = 0
            self.is_jumping = False

    def draw(self):
        self.sprite.draw()
