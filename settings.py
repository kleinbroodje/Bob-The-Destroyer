import pygame
from pathlib import Path


pygame.init()

WIDTH, HEIGHT = 400, 225
screen = pygame.display.set_mode((1280, 720))
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
            row_sheet = []
            for j in range(columns):
                frame = row.subsurface(
                    j * frame_width,
                    0,
                    frame_width,
                    frame_height,
                )
                row_sheet.append(frame)

            ret.append(row_sheet)

    return ret


def create_bloom(image, color, scale, rect):
    surf = pygame.transform.scale_by(pygame.mask.from_surface(image).to_surface(setcolor=color), scale)
    display.blit(surf, (rect.centerx - surf.width/2, rect.centery - surf.height/2), special_flags=pygame.BLEND_RGB_ADD)


class CooldownBar:
    def __init__(self, color, cooldown, label):
        self.max_bar = pygame.Rect(40, 0, 25, 6)
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

        display.blit(font[10].render(self.label, False, (255, 255, 255)), (self.bar.x - 30, self.bar.y-self.bar.height/2))
        pygame.draw.rect(display, self.color, self.bar)

