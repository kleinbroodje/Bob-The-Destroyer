import pygame
from pathlib import Path
from csv import reader


pygame.init()

WIDTH, HEIGHT = 400, 225
screen = pygame.display.set_mode((1280, 720))
ui_display = pygame.Surface((1280, 720))
display = pygame.Surface((WIDTH, HEIGHT)) 
pygame.display.set_caption("Bob The Destroyer")
R = screen.width/WIDTH #scale 
scroll = [0, 0]
cooldown_bars = []
font = [
    pygame.font.Font(Path("assets", "Micro5-Regular.ttf"), i)
    for i in range(101)
]


def imgload(*path, columns=1, rows=1):
    image = pygame.image.load(Path(*path)).convert_alpha()
     
    if columns * rows == 1: 
        return image
    else:
        frame_width = image.get_width() / columns
        frame_height = image.get_height() / rows

    ret = []
    if columns > 1 and rows == 1:  # if image is divided into columns
        for i in range(columns):
            sub = image.subsurface(
                i * frame_width,
                0,
                frame_width,
                frame_height,
            )
            ret.append(sub)

    elif rows > 1 and columns == 1:  # if image is divided into rows
        for i in range(rows):
            sub = image.subsurface(
                0,
                i * frame_height,
                frame_width,
                frame_height,
            )
            ret.append(sub)

    elif columns > 1 and rows > 1:  # if image is divided two-dimensinally
        ret = []
        for i in range(rows):
            row = image.subsurface(
                0, i * frame_height, image.get_width(), frame_height
            )
            for j in range(columns):
                frame = row.subsurface(
                    j * frame_width,
                    0,
                    frame_width,
                    frame_height,
                )
                ret.append(frame)
    return ret


def create_bloom(image, color, scale, rect):
    surf = pygame.transform.scale_by(pygame.mask.from_surface(image).to_surface(setcolor=color), scale)
    display.blit(surf, (rect.centerx - surf.width/2, rect.centery - surf.height/2), special_flags=pygame.BLEND_RGB_ADD)



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


tile_images = imgload("assets", "tileset.png", columns=5, rows=3)
basic_map = TileMap(Path("assets", "basic_map.csv"))


class CooldownBar:
    def __init__(self, color, cooldown, label):
        self.max_bar = pygame.Rect(45, 0, 25, 6)
        self.bar = self.max_bar.copy()
        self.color = color
        self.label = label
        self.cooldown = cooldown
        self.last_time = 0

    def update(self, time):
        r = (time-self.last_time)/self.cooldown
        self.bar.width = self.max_bar.width - self.max_bar.width * r
        if self.bar.width <= 0:
            cooldown_bars.remove(self)

        ui_display.blit(font[40].render(self.label, False, (255, 255, 255)), ((self.bar.x - 40)*R, (self.bar.y-self.bar.height/2)*R))
        pygame.draw.rect(display, self.color, self.bar)

