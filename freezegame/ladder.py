from pybaconSprite import PybaconSprite

class Ladder(PybaconSprite):
    def __init__(self, x, y, state):
        PybaconSprite.__init__(self, x, y, [0, 0, 32, 32], state, 'tileSet', [0, 160, 32, 32], state.batch, state.ladderGroup)
