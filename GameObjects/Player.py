import pyglet

from pyglet.window import key
from typing import Tuple

# Load all the sprite sheets for the player character
run_right_spritesheet = pyglet.image.load("GameObjects/Assets/assassin_run_right.png")
run_left_spritesheet = pyglet.image.load("GameObjects/Assets/assassin_run_left.png")
idle_spritesheet = pyglet.image.load("GameObjects/Assets/assassin_idle.png")
jump_spritesheet = pyglet.image.load("GameObjects/Assets/assassin_jump.png")
attack_spritesheet = pyglet.image.load("GameObjects/Assets/assassin_attack.png")
attack_left_spritesheet = pyglet.image.load("GameObjects/Assets/assassin_attack_left.png")
air_attack_spritesheet = pyglet.image.load("GameObjects/Assets/assassin_air_attack.png")
air_attack_left_spritesheet = pyglet.image.load("GameObjects/Assets/assassin_air_attack_left.png")
fall_spritesheet = pyglet.image.load("GameObjects/Assets/assassin_falling.png")
fall_left_spritesheet = pyglet.image.load("GameObjects/Assets/assassin_falling_left.png")
assassin_hit_spritesheet = pyglet.image.load("GameObjects/Assets/assassin_hit.png")
assassin_death_spritesheet = pyglet.image.load("GameObjects/Assets/assassin_death.png")

# Load all player-related sounds
air_attack_sound = pyglet.media.load('Resources/air_attack.wav', streaming=False)
jump_sound = pyglet.media.load('Resources/jump.wav', streaming=False)
player_hit_sound = pyglet.media.load('Resources/player_hit.wav', streaming=False)
sword_sound = pyglet.media.load('Resources/sword.wav', streaming=False)
player_lost_sound = pyglet.media.load('Resources/player_lost.wav', streaming=False)


# Calculate frame size for run animation
run_rows = 1
run_columns = 8

# Calculate frame size for idle animation
idle_rows = 1
idle_columns = 8

# Calculate frame size for jump animation
jump_rows = 1
jump_columns = 3

# Calculate frame size for attack animation
attack_rows = 1
attack_columns = 8

# Calculate frame size for air attack animation
air_attack_rows = 1
air_attack_columns = 7

# Calculate frame size for hit animation
hit_rows = 1
hit_columns = 6

# Calculate frame size for death animation
death_rows = 1
death_columns = 19

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
fall_image_grid = pyglet.image.ImageGrid(fall_spritesheet, jump_rows, jump_columns)
fall_textures = pyglet.image.TextureGrid(fall_image_grid)
fall_left_image_grid = pyglet.image.ImageGrid(fall_left_spritesheet, jump_rows, jump_columns)
fall_left_textures = pyglet.image.TextureGrid(fall_left_image_grid)

# Create image grids and textures for attack animations
attack_image_grid = pyglet.image.ImageGrid(attack_spritesheet, attack_rows, attack_columns)
attack_textures = pyglet.image.TextureGrid(attack_image_grid)
attack_left_image_grid = pyglet.image.ImageGrid(attack_left_spritesheet, attack_rows, attack_columns)
attack_left_textures = pyglet.image.TextureGrid(attack_left_image_grid)
air_attack_image_grid = pyglet.image.ImageGrid(air_attack_spritesheet, air_attack_rows, air_attack_columns)
air_attack_left_image_grid = pyglet.image.ImageGrid(air_attack_left_spritesheet, air_attack_rows, air_attack_columns)
air_attack_textures = pyglet.image.TextureGrid(air_attack_image_grid)
air_attack_textures_left = pyglet.image.TextureGrid(air_attack_left_image_grid)

# Create image grids and textures for hit animation
hit_image_grid = pyglet.image.ImageGrid(assassin_hit_spritesheet, hit_rows, hit_columns)
hit_textures = pyglet.image.TextureGrid(hit_image_grid)

# Create image grids and textures for death animation
death_image_grid = pyglet.image.ImageGrid(assassin_death_spritesheet, death_rows, death_columns)
death_textures = pyglet.image.TextureGrid(death_image_grid)


def detect_collision(player, object2):
    if not player.is_dying:
        if (player.sprite.x + player.sprite.width / 2 >= object2.sprite.x and
                player.sprite.x + player.sprite.width / 2 <= object2.sprite.x + object2.sprite.width and
                player.sprite.y + player.sprite.height / 5 >= object2.sprite.y and
                player.sprite.y + player.sprite.height / 5 <= object2.sprite.y + object2.sprite.height
                and object2.current_animation == object2.idle_animation):
            player.is_dying = True
            player_hit_sound.play()
            pyglet.clock.schedule_once(play_losing_sound, 1.0)
            return True

def play_losing_sound(dt):
    player_lost_sound.play()

class Player:
    def __init__(self, x, y, batch=None):
        self.player_initial_speed = 3
        self.jump_speed = 500
        self.is_jumping = False
        self.is_falling = False
        self.gravity = 1000
        self.initial_y = y
        self.is_running = False
        self.keys = {key.D: False, key.A: False, key.L: False,
                     key.K: False, key.SPACE: False}
        # Initialize velocity
        self.velocity_x = 0
        self.velocity_y = 0

        # Initialize dying state
        self.is_dying = False

        # Create run animation
        self.run_animation = pyglet.image.Animation.from_image_sequence(run_textures[0:], duration=0.1, loop=True)
        self.run_left_animation = pyglet.image.Animation.from_image_sequence(
            run_left_textures[run_columns:0:-1], duration=0.1,
            loop=True)

        # Create idle animation
        self.idle_animation = pyglet.image.Animation.from_image_sequence(idle_textures[0:], duration=0.1, loop=True)

        # Create jump animation
        self.jump_animation = pyglet.image.Animation.from_image_sequence(jump_textures[0:], duration=0.1, loop=False)

        # Create fall animations
        self.fall_animation = pyglet.image.Animation.from_image_sequence(fall_textures[0:], duration=0.1, loop=True)
        self.fall_left_animation = pyglet.image.Animation.from_image_sequence(fall_left_textures[jump_columns:0:-1],
                                                                              duration=0.1, loop=True)

        # Create attack animation
        self.attack_animation = pyglet.image.Animation.from_image_sequence(attack_textures[0:],
                                                                           duration=0.1, loop=False)
        self.attack_left_animation = pyglet.image.Animation.from_image_sequence(
            attack_left_textures[attack_columns:0:-1],
            duration=0.1, loop=False)

        self.air_attack_animation = pyglet.image.Animation.from_image_sequence(air_attack_textures[0:],
                                                                               duration=0.1, loop=True)
        self.air_attack_left_animation = pyglet.image.Animation.from_image_sequence(
            air_attack_textures_left[air_attack_columns:0:-1],
            duration=0.1, loop=True)

        # Create hit animation
        self.hit_animation = pyglet.image.Animation.from_image_sequence(hit_textures[0:], duration=0.1, loop=False)

        # Create death animation
        self.death_animation = pyglet.image.Animation.from_image_sequence(death_textures[0:], duration=0.1, loop=False)

        # Set initial animation to idle
        self.current_animation = self.idle_animation

        # Create sprite
        self.sprite = pyglet.sprite.Sprite(self.current_animation, x=x, y=y)
        self.player_width = self.sprite.width // 2

    def update(self, border, win_size: Tuple, dt, active_enemies, roller):
        # Update position based on velocity
        new_x = self.sprite.x + self.velocity_x * dt
        # Ensure player stays stuck in position
        if self.sprite.x < border - self.player_width:
            self.sprite.x = border - self.player_width
        elif self.sprite.x + self.player_width >= (win_size[0] - border) // 2:
            self.sprite.x = (win_size[0] - border) // 2 - self.player_width
            # self.sprite.x = win_size[0] - border - self.player_width
        else:
            self.sprite.x = new_x

        for enemy in active_enemies:
            if detect_collision(self, enemy):
                if not self.is_hit_animating():
                    self.play_hit_animation()

        if detect_collision(self, roller):
            if not self.is_hit_animating():
                self.play_hit_animation()
                # pyglet.clock.schedule_once(self.hit_animation_complete, self.hit_animation.get_duration())
        # Check if the player is jumping
        if self.is_jumping:
            # Update the jump behavior
            self.sprite.y += self.velocity_y * dt
            self.update_jump(dt)
            self.velocity_y -= self.gravity * dt

    def on_key_press(self, symbol, modifiers):
        if not self.is_dying:
            # Check if the pressed key is left or right arrow
            if symbol == key.D:
                self.keys[symbol] = True
                if not self.is_jumping:
                    self.velocity_x = abs(self.player_initial_speed)
                    self.current_animation = self.run_animation
                    self.sprite.image = self.run_animation
            elif symbol == key.A:
                self.keys[symbol] = True
                if not self.is_jumping:
                    self.velocity_x = -abs(self.player_initial_speed)
                    self.current_animation = self.run_left_animation
                    self.sprite.image = self.run_left_animation

            elif symbol == key.K:
                if not self.keys[symbol]:
                    self.keys[symbol] = True
                    if self.keys[key.A]:
                        if self.is_jumping:
                            self.current_animation = self.air_attack_left_animation
                            self.sprite.image = self.air_attack_left_animation
                            air_attack_sound.play()
                        else:
                            self.current_animation = self.attack_left_animation
                            self.sprite.image = self.attack_left_animation
                            sword_sound.play()
                    elif self.keys[key.D]:
                        if self.is_jumping:
                            self.current_animation = self.air_attack_animation
                            self.sprite.image = self.air_attack_animation
                            air_attack_sound.play()
                        else:
                            self.current_animation = self.attack_animation
                            self.sprite.image = self.attack_animation
                            sword_sound.play()
                    elif self.is_jumping:
                        self.current_animation = self.air_attack_animation
                        self.sprite.image = self.air_attack_animation
                        air_attack_sound.play()
                    else:
                        self.current_animation = self.attack_animation
                        self.sprite.image = self.attack_animation
                        sword_sound.play()

                    pyglet.clock.schedule_once(self.attack_animation_complete, self.attack_animation.get_duration())

            elif symbol == key.SPACE:
                if not self.keys[symbol]:
                    self.keys[symbol] = True
                    self.jump()
            elif symbol == key.L:
                if not self.keys[symbol]:
                    self.keys[symbol] = True
            if self.keys[key.L] and not self.is_running and not self.is_jumping:
                self.is_running = True
                if self.velocity_x > 0:
                    self.velocity_x = self.player_initial_speed * 2
                elif self.velocity_x < 0:
                    self.velocity_x = -self.player_initial_speed * 2

    def on_key_release(self, symbol, modifiers):
        if not self.is_dying:
            # Check if the released key is left or right arrow
            if symbol in (key.D, key.A):
                self.keys[symbol] = False
                if not self.is_jumping:
                    self.velocity_x = 0
                    self.current_animation = self.idle_animation
                    self.sprite.image = self.idle_animation
            elif symbol == key.SPACE:
                self.keys[symbol] = False
                if self.keys[pyglet.window.key.D] and self.sprite.y == self.initial_y:
                    self.current_animation = self.run_animation
                    self.sprite.image = self.run_animation
                elif self.keys[pyglet.window.key.A] and self.sprite.y == self.initial_y:
                    self.current_animation = self.run_left_animation
                    self.sprite.image = self.run_left_animation
                elif self.sprite.y == self.initial_y:
                    self.current_animation = self.idle_animation
                    self.sprite.image = self.idle_animation

            elif symbol == key.L:
                if self.is_running:
                    self.keys[key.L] = False
                # Schedule the statement to be executed after 1 second
                pyglet.clock.schedule_once(self.stop_running, 2.0)
        else:
            self.velocity_x = 0
            self.velocity_y = 0


    def attack_animation_complete(self, dt):
        # This method will be called when the attack animation is complete
        self.keys[key.K] = False
        self.return_to_proper_animation()

    def jump(self):
        if not self.is_jumping:
            jump_sound.play()
            self.velocity_y = self.jump_speed
            self.is_jumping = True
            self.current_animation = self.jump_animation
            self.sprite.image = self.jump_animation

    def update_jump(self, dt):
        if not self.is_dying:
            if self.sprite.y >= 159 and not self.is_falling and not self.keys[key.K]:
                self.is_falling = True
                if self.velocity_x >= 0:
                    self.current_animation = self.fall_animation
                    self.sprite.image = self.fall_animation
                else:
                    self.current_animation = self.fall_left_animation
                    self.sprite.image = self.fall_left_animation
            # Check if the player has ascended above or descended below the initial y position
            if self.sprite.y <= self.initial_y:
                self.is_falling = False
                # If descending below, reset to initial y position and stop the jump
                self.sprite.y = self.initial_y
                self.velocity_y = 0
                self.velocity_x = 0
                self.is_jumping = False
                if (not self.current_animation == self.attack_animation
                        and not self.current_animation == self.attack_left_animation):
                    if self.keys[pyglet.window.key.D]:
                        self.velocity_x = abs(self.player_initial_speed)
                        self.current_animation = self.run_animation
                        self.sprite.image = self.run_animation
                    elif self.keys[pyglet.window.key.A]:
                        self.velocity_x = -abs(self.player_initial_speed)
                        self.current_animation = self.run_left_animation
                        self.sprite.image = self.run_left_animation
                    else:
                        self.current_animation = self.idle_animation
                        self.sprite.image = self.idle_animation
        else:
            self.sprite.y = self.initial_y

    def play_hit_animation(self):
        self.current_animation = self.hit_animation
        self.sprite.image = self.hit_animation
        pyglet.clock.schedule_once(self.hit_animation_complete, self.hit_animation.get_duration())

    def is_hit_animating(self):
        return self.current_animation == self.hit_animation

    def hit_animation_complete(self, dt):
        self.return_to_proper_animation()

    def die(self):
        self.current_animation = self.death_animation
        self.sprite.image = self.death_animation
        self.velocity_x = 0
        self.velocity_y = 0

    def return_to_proper_animation(self):
        if self.is_dying:
            self.die()
            return
        if self.keys[key.A]:
            if self.is_running:
                self.velocity_x = -self.player_initial_speed * 2
            else:
                self.velocity_x = -self.player_initial_speed
            self.current_animation = self.run_left_animation
            self.current_animation = self.run_left_animation
            self.sprite.image = self.run_left_animation
        elif self.keys[key.D]:
            if self.is_running:
                self.velocity_x = self.player_initial_speed * 2
            else:
                self.velocity_x = self.player_initial_speed
            self.current_animation = self.run_animation
            self.sprite.image = self.run_animation
        else:
            self.current_animation = self.idle_animation
            self.sprite.image = self.idle_animation

    def stop_running(self, dt):
        self.is_running = False
        if not self.is_jumping:
            if self.keys[key.A]:
                self.velocity_x = -self.player_initial_speed
            elif self.keys[key.D]:
                self.velocity_x = self.player_initial_speed

    def draw(self):
        self.sprite.draw()
