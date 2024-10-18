import tomllib
from math import atan2, cos, sin, degrees, radians

from settings import *


class Weapon:
    def __init__(self, name, offset):
        self.name = name
        self.image = imgload('assets', f"{self.name}.png", scale=1)
        self.offset = offset

    def update(self, x, y):
        mouse_pos = pygame.mouse.get_pos()
        angle = degrees(atan2(-(mouse_pos[1]-y), mouse_pos[0]-x))

        if angle > 90 or angle < -90:
            image = pygame.transform.flip(self.image, True, False)
            image = pygame.transform.rotate(image, angle + 180)
        else:
            image = pygame.transform.rotate(self.image, angle)

        image = pygame.transform.scale_by(image, R)
        image_rect = image.get_rect(center=(x + cos(radians(angle)) * 37, y - sin(radians(angle)) * 32))
        
        display.blit(image, image_rect)

with open("weapons.toml", "rb") as f:
    weapon_data = tomllib.load(f)
    weapons = {}
    for k, v in weapon_data.items():
        weapons[k] = Weapon(k, v["offset"])
