from freezegame.sprite import Sprite


class Tile(Sprite):
    def __init__(self, x, y, box, state, image_name=None, image_region=None, batch=None, group=None):
        Sprite.__init__(self, x, y, box, state, image_name, image_region, batch, group)
        self.tile = True
