import tomllib
from random import uniform
from math import atan2, cos, sin, degrees, radians

from settings import *


bullets = []


class Weapon:
    def __init__(self, name, weapon_type, bullet_type, bullet_speed, spread, rotation):
        self.name = name
        self.image = imgload("assets", f"{self.name}.png", scale=1)
        self.rect = self.image.get_rect()
        self.width = self.rect.width
        self.weapon_type = weapon_type
        self.bullet_type = bullet_type
        self.bullet_speed = bullet_speed
        self.spread = spread 
        self.angle = 0
        self.rotation = rotation

    def is_auto(self):
        return weapon_data[self.name]["auto"]
    
    def shoot(self):
        match self.weapon_type:
            case "shotgun":
                for i in range(3):
                    bullets.append(Bullet(self.rect.centerx + cos(radians(self.angle)) * self.width, 
                                          self.rect.centery - sin(radians(self.angle)) * self.width,
                                          self.bullet_type, 
                                          self.angle, 
                                          self.bullet_speed, 
                                          self.spread
                                    ))

    def update(self, x, y):
        mouse_pos = pygame.mouse.get_pos()
        self.angle = degrees(atan2(-(mouse_pos[1]-y), mouse_pos[0]-x))

        if self.angle > 90 or self.angle < -90:
            image = pygame.transform.flip(self.image, True, False)
            image = pygame.transform.rotate(image, self.angle + 180)
        else:
            image = pygame.transform.rotate(self.image, self.angle)

        image = pygame.transform.scale_by(image, R)
        self.rect = image.get_rect(center=(x + cos(radians(self.angle)) * self.rotation[1], y - sin(radians(self.angle)) * self.rotation[0]))
        #pygame.draw.rect(display, (255, 0, 0), self.rect, 2)
        display.blit(image, self.rect)


class Bullet:
    def __init__(self, x, y, bullet_type, angle, speed, spread):
        self.bullet_type = bullet_type
        self.angle = angle + uniform(-spread, spread)
        self.image = imgload("assets", f"{self.bullet_type}_bullet.png", scale=1)
        self.image = pygame.transform.scale_by(pygame.transform.rotate(self.image, self.angle), R)
        self.img_rect = self.image.get_rect()
        self.rect = pygame.Rect(0, 0, self.img_rect.width-2*R, self.img_rect.height-2*R)
        self.rect.center = x, y
        self.vel_x = cos(radians(self.angle)) * speed
        self.vel_y = sin(radians(self.angle)) * speed

    def update(self):
        self.rect.x+= self.vel_x
        self.rect.y -= self.vel_y

        if (self.rect.centerx > WIDTH or self.rect.centerx < 0) and (self.rect.centery > HEIGHT or self.rect.centery < 0):
            bullets.remove(self)

        display.blit(self.image, self.rect)


with open("weapons.toml", "rb") as f:
    weapon_data = tomllib.load(f)
    weapons = {}
    for k, v in weapon_data.items():
        weapons[k] = Weapon(k, v["weapon_type"], v["bullet_type"], v["bullet_speed"], v["spread"], v["rotation"])
