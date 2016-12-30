from freezegame.sprite import Sprite


class Ladder(Sprite):
    def __init__(self, x, y, state):
        Sprite.__init__(self, x, y, [0, 0, 32, 32], state, 'tileSet', [0, 160, 32, 32], state.batch, state.ladder_group)
