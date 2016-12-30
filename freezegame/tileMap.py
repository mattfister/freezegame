import pyglet
import math
import random
from pybaconSprite import PybaconSprite
from tile import Tile
from autoTiler import AutoTiler

class TileMap():
    def __init__(self, tileWidth, tileHeight, width, height, state, tileSet, imageRegion, group):
        self.tileWidth = tileWidth
        self.tileHeight = tileHeight
        
        self.width = width
        self.height = height
        
        self.state = state
        self.batch = self.state.batch
        self.group = group
        
        self.tileSet = tileSet
        self.imageRegion = imageRegion
        
        self.tiles = []
        self.autotiler = AutoTiler() 
        for i in range(self.width):
            self.tiles.append([])
            for j in range(self.height):
                newTile = None
                self.tiles[i].append(newTile)
        
    def buildSurroundingWalls(self):
        for i in range(self.width):
            for j in range(self.height):
                if i == 0 or i== self.width -1 or j == 0 or j == self.height-1:
                    newTile = Tile(i*self.tileWidth, j*self.tileHeight, [0, 0, self.tileWidth, self.tileHeight], self.state, self.tileSet, self.imageRegion, self.batch, self.group)
                    newTile.invincible = True
                    self.tiles[i][j] = newTile
    
    def fill(self):
        for i in range(self.width):
            for j in range(self.height):
                newTile = Tile(i*self.tileWidth, j*self.tileHeight, [0, 0, self.tileWidth, self.tileHeight], self.state, self.tileSet, self.imageRegion, self.batch, self.group)
                self.tiles[i][j] = newTile
                
    def prepForPickle(self):
        self.state = None
        self.batch = None
        self.group = None
        for i in range(self.width):
            for j in range(self.height):
                if self.tiles[i][j] != None:
                    self.tiles[i][j].prepForPickle()
    
    def restoreFromPickle(self, state, group):
        self.state = state
        self.batch = self.state.batch
        self.group = group
        for i in range(self.width):
            for j in range(self.height):
                if self.tiles[i][j] != None:
                    self.tiles[i][j].restoreFromPickle(self.state, group)
    
    def update(self, dt, keys, state):
        pass

    def tileCoordForPosition(self, pos):
        x = int(math.floor(float(pos[0]) / float(self.tileWidth )))
        y = int(math.floor(float(pos[1]) / float(self.tileHeight)));
        return [x, y]

    def getTile(self, coord):
        if not self.validTile(coord):
            return None
        return self.tiles[coord[0]][coord[1]]
    
    def getTileForPos(self, pos):
        coord = self.tileCoordForPosition(pos)
        return self.getTile(coord)
    
    def getSurroundingTilesByPos(self, pos):
        coord = self.tileCoordForPosition(pos)
        surroundingTiles = []
        
        surroundingTiles.append(self.getTile([coord[0], coord[1]-1]))
        surroundingTiles.append(self.getTile([coord[0], coord[1]+1]))
        surroundingTiles.append(self.getTile([coord[0]-1, coord[1]]))
        surroundingTiles.append(self.getTile([coord[0]+1, coord[1]]))
        surroundingTiles.append(self.getTile([coord[0]-1, coord[1]+1]))
        surroundingTiles.append(self.getTile([coord[0]+1, coord[1]+1]))
        surroundingTiles.append(self.getTile([coord[0]-1, coord[1]-1]))
        surroundingTiles.append(self.getTile([coord[0]+1, coord[1]-1]))
        surroundingTiles.append(self.getTile([coord[0], coord[1]]))
        
        return surroundingTiles
    
    def getRadiusTwoSurroundingTilesForPos(self, pos):
        coord = self.tileCoordForPosition(pos)
        surroundingTiles = []
        surroundingTiles.append(self.getTile([coord[0], coord[1]-2]))
        surroundingTiles.append(self.getTile([coord[0], coord[1]-1]))
        surroundingTiles.append(self.getTile([coord[0], coord[1]+1]))
        surroundingTiles.append(self.getTile([coord[0], coord[1]+2]))

        surroundingTiles.append(self.getTile([coord[0]-1, coord[1]]))
        surroundingTiles.append(self.getTile([coord[0]-2, coord[1]]))

        surroundingTiles.append(self.getTile([coord[0]+1, coord[1]]))
        surroundingTiles.append(self.getTile([coord[0]+2, coord[1]]))

        surroundingTiles.append(self.getTile([coord[0]-1, coord[1]+1]))
        surroundingTiles.append(self.getTile([coord[0]+1, coord[1]+1]))
        surroundingTiles.append(self.getTile([coord[0]-1, coord[1]-1]))
        surroundingTiles.append(self.getTile([coord[0]+1, coord[1]-1]))
        surroundingTiles.append(self.getTile([coord[0], coord[1]]))
        
        return surroundingTiles
        
    
    def removeTileForPos(self, pos):
        coord = self.tileCoordForPosition(pos)
        self.removeTile(*coord)
        
    def removeTile(self, tileX, tileY):
        if self.tiles[tileX][tileY] != None:
            if self.tiles[tileX][tileY].invincible == False:
                self.tiles[tileX][tileY].sprite.delete()
                self.tiles[tileX][tileY] = None
        
    def validTile(self, coord):
        if coord[0] < 0:
            return False
        if coord[0] >= self.width:
            return False
        if coord[1] < 0:
            return False
        if coord[1] >= self.height:
            return False
        return True
    
    def makeTile(self, tileX, tileY):
        if self.validTile([tileX, tileY]):
            if self.tiles[tileX][tileY] == None:
                self.tiles[tileX][tileY] = Tile(tileX*self.tileWidth, tileY*self.tileHeight, [0, 0, self.tileWidth, self.tileHeight], self.state, self.tileSet, self.imageRegion, self.batch, self.group)
                
    
    def autoTile(self):
        self.autotiler.auto_tile(self)
        
    def getStraightPath(self, startPos, endPos):
        [startX, startY] = self.tileCoordForPosition(startPos)
        [x, y] = self.tileCoordForPosition(endPos)
        path = []
        x0 = startX + 0.5
        y0 = startY + 0.5
        x1 = x + 0.5
        y1 = y + 0.5
        
        dx = abs(x1 - x0)
        dy = abs(y1 - y0)
        
        x = int(math.floor(x0))
        y = int(math.floor(y0))
        
        n = 1
        
        xInc = 0
        yInc = 0
        
        error = 0.0
        
        if (dx == 0):
            xInc = 0
            error = float('inf')
        elif (x1 > x0):
            xInc = 1
            n += int(math.floor(x1)) - x
            error = (math.floor(x0) + 1 - x0) * dy
        else:
            xInc = -1
            n += x - int(math.floor(x1))
            error = (x0 - math.floor(x0)) * dy
            
            
        if (dy == 0):
            yInc = 0
            error = float('-inf')
        elif (y1 > y0):
            yInc = 1
            n += int(math.floor(y1)) - y
            error -= (math.floor(y0) + 1 - y0) * dx
        else:
            yInc = -1
            n += y - int(math.floor(y1))
            error -= (y0 - math.floor(y0)) * dx
        
        while n > 0:
            n -= 1
            path.append([x, y])
            if self.getTile([x, y]) != None:
                return None
            if (error > 0):
                y += yInc
                error -= dx
            else:
                x += xInc
                error += dy
        return path