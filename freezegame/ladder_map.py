from freezegame.tile_map import TileMap
from freezegame.ladder import Ladder


class LadderMap(TileMap):
    def __init__(self, tile_width, tile_height, width, height, state, tile_set, image_region, group):
        TileMap.__init__(self, tile_width, tile_height, width, height, state, tile_set, image_region, group)
        self.ladders = []

    def update(self, dt, keys, state):
        for sprite in self.power_sources + self.connectors:
            sprite.update(dt, keys, state)

    def pick_ladder(self, x, y):
        for sprite in self.wires:
            if sprite.collides_point(x, y):
                return sprite
        return None

    def make_ladder(self, tileX, tileY):
        if self.validTile([tileX, tileY]):
            ladder = Ladder(tileX * self.tile_width, tileY * self.tile_height, self.state)
            self.tiles[tileX][tileY] = ladder
