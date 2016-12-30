import pyglet
import math
import random
from pybacon.pybaconSprite import PybaconSprite
from pybacon.auto_tiler import AutoTiler
from pybacon.tileMap import TileMap
from ladder import Ladder

class LadderMap(TileMap):
    def __init__(self, tileWidth, tileHeight, width, height, state, tileSet, imageRegion, group):
        TileMap.__init__(self, tileWidth, tileHeight, width, height, state, tileSet, imageRegion, group)
        self.ladders = []
        
    def update(self, dt, keys, state):        
        for sprite in self.powerSources + self.connectors:
            sprite.update(dt, keys, state)
    
    def pickLadder(self, x, y):
        for sprite in self.wires:
            if sprite.collidesPoint(x, y):
                return sprite
        return None
        
    def makeLadder(self, tileX, tileY):
        if self.validTile([tileX, tileY]):
            ladder = Ladder(tileX*self.tileWidth, tileY*self.tileHeight, self.state)
            self.tiles[tileX][tileY] = ladder
            