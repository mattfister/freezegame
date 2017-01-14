import math
from freezegame.tile import Tile
from freezegame.auto_tiler import AutoTiler


class TileMap:
    def __init__(self, tile_width, tile_height, width, height, state, tile_set, image_region, group):
        self.tile_width = tile_width
        self.tile_height = tile_height

        self.width = width
        self.height = height

        self.state = state
        self.batch = self.state.batch
        self.group = group

        self.tileSet = tile_set
        self.imageRegion = image_region

        self.tiles = []
        self.autotiler = AutoTiler()
        for i in range(self.width):
            self.tiles.append([])
            for j in range(self.height):
                new_tile = None
                self.tiles[i].append(new_tile)

    def build_surrounding_walls(self):
        for i in range(self.width):
            for j in range(self.height):
                if i == 0 or i == self.width - 1 or j == 0 or j == self.height - 1:
                    new_tile = Tile(i * self.tile_width, j * self.tile_height, [0, 0, self.tile_width, self.tile_height],
                                    self.state, self.tileSet, self.imageRegion, self.batch, self.group)
                    self.tiles[i][j] = new_tile

    def fill(self):
        for i in range(self.width):
            for j in range(self.height):
                new_tile = Tile(i * self.tile_width, j * self.tile_height, [0, 0, self.tile_width, self.tile_height],
                                self.state, self.tileSet, self.imageRegion, self.batch, self.group)
                self.tiles[i][j] = new_tile

    def prep_for_pickle(self):
        self.state = None
        self.batch = None
        self.group = None
        for i in range(self.width):
            for j in range(self.height):
                if self.tiles[i][j] is not None:
                    self.tiles[i][j].prep_for_pickle()

    def restore_from_pickle(self, state, group):
        self.state = state
        self.batch = self.state.batch
        self.group = group
        for i in range(self.width):
            for j in range(self.height):
                if self.tiles[i][j] is not None:
                    self.tiles[i][j].restore_from_pickle(self.state, group)

    def update(self, dt, keys, state):
        pass

    def tile_coord_for_position(self, pos):
        x = int(math.floor(float(pos[0]) / float(self.tile_width)))
        y = int(math.floor(float(pos[1]) / float(self.tile_height)));
        return [x, y]

    def get_tile(self, coord):
        if not self.valid_tile(coord):
            return None
        return self.tiles[coord[0]][coord[1]]

    def get_tile_for_pos(self, pos):
        coord = self.tile_coord_for_position(pos)
        return self.get_tile(coord)

    def get_surrounding_tiles_by_pos(self, pos):
        coord = self.tile_coord_for_position(pos)
        surrounding_tiles = [self.get_tile([coord[0], coord[1] - 1]), self.get_tile([coord[0], coord[1] + 1]),
                             self.get_tile([coord[0] - 1, coord[1]]), self.get_tile([coord[0] + 1, coord[1]]),
                             self.get_tile([coord[0] - 1, coord[1] + 1]), self.get_tile([coord[0] + 1, coord[1] + 1]),
                             self.get_tile([coord[0] - 1, coord[1] - 1]), self.get_tile([coord[0] + 1, coord[1] - 1]),
                             self.get_tile([coord[0], coord[1]])]

        return surrounding_tiles

    def get_radius_two_surrounding_tiles_for_pos(self, pos):
        coord = self.tile_coord_for_position(pos)
        surrounding_tiles = [self.get_tile([coord[0], coord[1] - 2]), self.get_tile([coord[0], coord[1] - 1]),
                             self.get_tile([coord[0], coord[1] + 1]), self.get_tile([coord[0], coord[1] + 2]),
                             self.get_tile([coord[0] - 1, coord[1]]), self.get_tile([coord[0] - 2, coord[1]]),
                             self.get_tile([coord[0] + 1, coord[1]]), self.get_tile([coord[0] + 2, coord[1]]),
                             self.get_tile([coord[0] - 1, coord[1] + 1]), self.get_tile([coord[0] + 1, coord[1] + 1]),
                             self.get_tile([coord[0] - 1, coord[1] - 1]), self.get_tile([coord[0] + 1, coord[1] - 1]),
                             self.get_tile([coord[0], coord[1]])]

        return surrounding_tiles

    def remove_tile_for_pos(self, pos):
        coord = self.tile_coord_for_position(pos)
        self.remove_tile(*coord)

    def remove_tile(self, tile_x, tile_y):
        if self.tiles[tile_x][tile_y] is not None:
            if not self.tiles[tile_x][tile_y].invincible:
                self.tiles[tile_x][tile_y].sprite.delete()
                self.tiles[tile_x][tile_y] = None

    def valid_tile(self, coord):
        if coord[0] < 0:
            return False
        if coord[0] >= self.width:
            return False
        if coord[1] < 0:
            return False
        if coord[1] >= self.height:
            return False
        return True

    def make_tile(self, tile_x, tile_y):
        if self.valid_tile([tile_x, tile_y]):
            if self.tiles[tile_x][tile_y] is None:
                self.tiles[tile_x][tile_y] = Tile(tile_x * self.tile_width, tile_y * self.tile_height,
                                                [0, 0, self.tile_width, self.tile_height], self.state, self.tileSet,
                                                self.imageRegion, self.batch, self.group)

    def auto_tile(self):
        self.autotiler.auto_tile(self)

    def get_straight_path(self, start_pos, end_pos):
        [start_x, start_y] = self.tile_coord_for_position(start_pos)
        [x, y] = self.tile_coord_for_position(end_pos)
        path = []
        x0 = start_x + 0.5
        y0 = start_y + 0.5
        x1 = x + 0.5
        y1 = y + 0.5

        dx = abs(x1 - x0)
        dy = abs(y1 - y0)

        x = int(math.floor(x0))
        y = int(math.floor(y0))

        n = 1

        x_inc = 0
        y_inc = 0

        error = 0.0

        if dx == 0:
            x_inc = 0
            error = float('inf')
        elif x1 > x0:
            x_inc = 1
            n += int(math.floor(x1)) - x
            error = (math.floor(x0) + 1 - x0) * dy
        else:
            x_inc = -1
            n += x - int(math.floor(x1))
            error = (x0 - math.floor(x0)) * dy

        if dy == 0:
            y_inc = 0
            error = float('-inf')
        elif y1 > y0:
            y_inc = 1
            n += int(math.floor(y1)) - y
            error -= (math.floor(y0) + 1 - y0) * dx
        else:
            y_inc = -1
            n += y - int(math.floor(y1))
            error -= (y0 - math.floor(y0)) * dx

        while n > 0:
            n -= 1
            path.append([x, y])
            if self.get_tile([x, y]) is not None:
                return None
            if error > 0:
                y += y_inc
                error -= dx
            else:
                x += x_inc
                error += dy
        return path
