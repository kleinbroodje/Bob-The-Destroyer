import tomllib
from random import uniform
from math import atan2, cos, sin, tan, degrees, radians, sqrt

from settings import *


bullets = []
projectiles = []

class Weapon:
    def __init__(self, name, weapon_type, bullet_type, bullet_speed, bullet_damage, spread, rotation):
        self.name = name
        self.image = imgload("assets", f"{self.name}.png", scale=1)
        self.rect = self.image.get_rect()
        self.width = self.rect.width
        self.weapon_type = weapon_type
        self.bullet_type = bullet_type
        self.bullet_speed = bullet_speed
        self.bullet_damage = bullet_damage
        self.spread = spread 
        self.angle = 0
        self.rotation = rotation

    def is_auto(self):
        return weapon_data[self.name]["auto"]
    
    def shoot(self):
        match self.weapon_type:
            case "shotgun":
                    self.angle -= 20
                    for i in range(3):
                        bullets.append(Bullet(self.rect.centerx + cos(radians(self.angle)) * self.width, 
                                            self.rect.centery - sin(radians(self.angle)) * self.width,
                                            self.bullet_type, 
                                            self.bullet_damage,
                                            self.angle, 
                                            self.bullet_speed, 
                                            self.spread
                                        ))
                        self.angle += 20

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
    def __init__(self, x, y, bullet_type, damage, angle, speed, spread):
        self.bullet_type = bullet_type
        self.angle = angle + uniform(-spread, spread)
        self.image = imgload("assets", f"{self.bullet_type}_bullet.png", scale=1)
        self.image = pygame.transform.scale_by(pygame.transform.rotate(self.image, self.angle), R)
        self.rect = self.image.get_rect()
        self.rect.center = x, y
        self.vel_x = cos(radians(self.angle)) * speed
        self.vel_y = sin(radians(self.angle)) * speed
        self.damage = damage

    def update(self):
        self.rect.x += self.vel_x
        self.rect.y -= self.vel_y

        if self.rect.centerx > WIDTH or self.rect.centerx < 0 or self.rect.centery > HEIGHT or self.rect.centery < 0:
            bullets.remove(self)

        #pygame.draw.rect(display, (255, 0, 0), self.rect, 2)
        if self.bullet_type == "default":
            create_bloom(self.image, (20, 20, 15), 2, self.rect)
        display.blit(self.image, self.rect)


class Projectile:
    def __init__(self, x, y, target_x, target_y, angle):
        self.rect = pygame.Rect(x, y, 30, 30)
        self.gravity = 1

        d = target_x-x
        t = sqrt((2*(tan(angle)*abs(d)+abs(y-target_y)))/self.gravity)
        v = d/(t*cos(angle))
        #v = sqrt(abs(d)*self.gravity/sin(2*angle))

        self.vel_x = v*cos(angle)
        self.vel_y = abs(v)*sin(angle)

    def update(self):
        self.vel_y -= self.gravity
        self.rect.y -= self.vel_y

        self.rect.x += self.vel_x

        if self.rect.centerx > WIDTH or self.rect.centerx < 0 or self.rect.centery > 396:
            projectiles.remove(self)

        pygame.draw.rect(display, (255, 0, 255), self.rect)


with open("weapons.toml", "rb") as f:
    weapon_data = tomllib.load(f)
    weapons = {}
    for k, v in weapon_data.items():
        weapons[k] = Weapon(k, v["weapon_type"], v["bullet_type"],v["bullet_speed"], v["bullet_damage"], v["spread"], v["rotation"])
