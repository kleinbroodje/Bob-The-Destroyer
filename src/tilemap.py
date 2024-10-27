from csv import reader

from .settings import *


class Tile:
    def __init__(self, image, x, y):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def draw(self, surface):
        surface.blit(self.image, self.rect)


class TileMap:
    def __init__(self, path):
        self.tile_size = 16
        self.tiles = self.load_tiles(path)
        self.map_surface = pygame.Surface((self.map_w, self.map_h)).convert()
        self.map_surface.set_colorkey((0, 0, 0))
        self.load_map()

    def read_csv(self, path):
        with open(path) as data:
            map_ = []
            data = reader(data, delimiter=",")
            for row in data:
                map_.append(list(row))
        return map_
    
    def load_map(self):
        for tile in self.tiles:
            tile.draw(self.map_surface)

    def load_tiles(self, path):
        tiles = []
        map_ = self.read_csv(path)
        x, y = 0, 0
        for row in map_:
            x = 0
            for tile in row:
                if tile != "-1":
                    tiles.append(Tile(tile_images[int(tile)], x * self.tile_size, y * self.tile_size))
                x += 1
            y += 1
        self.map_w = x * self.tile_size
        self.map_h = y * self.tile_size
        return tiles

    def update(self):
        display.blit(self.map_surface, (0-scroll[0], 0-scroll[1]))


tile_images = imgload("assets", "images", "tileset.png", columns=5, rows=3)
basic_map = TileMap(Path("assets", "tilemaps", "basic_map.csv"))