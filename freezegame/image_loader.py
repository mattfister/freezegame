import pyglet
import os


# This function disables the default bilinear filtering on textures, so scaled textures maintain pixelly goodness
def texture_set_mag_filter_nearest(texture):
    pyglet.gl.glBindTexture(texture.target, texture.id)
    pyglet.gl.glTexParameteri(texture.target, pyglet.gl.GL_TEXTURE_MAG_FILTER, pyglet.gl.GL_NEAREST)
    pyglet.gl.glBindTexture(texture.target, 0)


class ImageLoader(object):
    def __init__(self, path):
        for file in os.listdir('./' + path):
            name = file.split('.')[0]
            image = pyglet.resource.image(file)
            texture_set_mag_filter_nearest(image.get_texture())
            self.__dict__[name] = image
