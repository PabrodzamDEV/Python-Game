import pyglet

# Class for the game's walls
class Wall(pyglet.shapes.Rectangle):

    def __init__(self, *args, **kwargs):
        super(Wall, self).__init__(*args, **kwargs)
