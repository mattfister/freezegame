class AutoTiler:
    def __init__(self):
        self.autoMap = {'UDLR': 0, 'DLR': 32, 'UDL': 64, 'ULR': 96, 'UDR': 128, 'DL': 160, 'UL': 192, 'UR': 224,
                        'DR': 256, 'LR': 288, 'UD': 320, 'U': 352, 'R': 384, 'D': 416, 'L': 448, '': 480}

    def auto_tile(self, tile_map):
        # Do base terrain/void transitions
        for i in range(0, tile_map.width):
            for j in range(0, tile_map.height):
                if not tile_map.get_tile([i, j]) is None and tile_map.get_tile([i, j]).tileable:
                    tile_string = ''
                    if not tile_map.valid_tile([i, j + 1]) or tile_map.get_tile([i, j + 1]) is not None:
                        tile_string += 'U'
                    if not tile_map.valid_tile([i, j - 1]) or tile_map.get_tile([i, j - 1]) is not None:
                        tile_string += 'D'
                    if not tile_map.valid_tile([i - 1, j]) or tile_map.get_tile([i - 1, j]) is not None:
                        tile_string += 'L'
                    if not tile_map.valid_tile([i + 1, j]) or tile_map.get_tile([i + 1, j]) is not None:
                        tile_string += 'R'
                    image_region = tile_map.tiles[i][j].image_region
                    image_region[0] = self.autoMap[tile_string]
                    tile_map.tiles[i][j].set_sprite(tile_map.tiles[i][j].image_name, image_region,
                                                   batch=tile_map.tiles[i][j].batch, group=tile_map.tiles[i][j].group)
