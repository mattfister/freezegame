from pybaconSprite import PybaconSprite

class Tile(PybaconSprite):
    def __init__(self, x, y, box, state, imageName = None, imageRegion = None, batch = None, group = None):
        PybaconSprite.__init__(self, x, y, box, state, imageName, imageRegion, batch, group)
        self.tile = True