from GameObjects.Roller import Roller
from GameObjects.Enemy import Enemy
from GameObjects.Player import Player
from GameObjects.Wall import Wall
from typing import Tuple


def load_walls(win_size: Tuple, border: float, batch=None):
    walls = []
    top = Wall(x=0, y=win_size[1] - border, width=win_size[0], height=border, batch=batch)
    left = Wall(x=0, y=0, width=border, height=win_size[1], batch=batch)
    right = Wall(x=win_size[0] - border, y=0, width=border, height=win_size[1], batch=batch)
    bottom = Wall(x=0, y=0, width=win_size[0], height=border, batch=batch)
    walls.extend([left, top, right, bottom])
    return walls


def load_player(x, y, batch=None):
    player = Player(x, y, batch)
    return player


def load_enemy(x, y, batch=None):
    enemy = Enemy(x, y, batch)
    return enemy


def load_roller(x, y, batch=None):
    roller = Roller(x, y, batch)
    return roller
