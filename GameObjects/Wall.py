import pyglet


# Class for the game's walls
class Wall(pyglet.shapes.Rectangle):

    def __init__(self, *args, texture=None, **kwargs):
        super(Wall, self).__init__(*args, **kwargs)
        self.texture = texture

        if self.texture is not None:
            self.image = self.create_texture()

    def create_texture(self):
        # Load the image and create a texture
        image = pyglet.image.load(self.texture)
        texture = image.get_texture()

        return texture
