import tomllib
from random import uniform
from math import atan2, cos, sin, tan, degrees, radians, sqrt

from .settings import *
from .tilemap import *


bullets = []
enemy_projectiles = []


class Weapon:
    def __init__(self, name):
        self.name = name
        self.image = imgload("assets", "images", f"{self.name}.png")
        self.rect = self.image.get_rect()
        self.width = self.rect.width
        self.weapon_type = weapon_data[self.name]["weapon_type"]
        self.angle = 0
        self.rotation = weapon_data[self.name]["rotation"]
        self.bullets_fired = weapon_data[self.name]["bullets_fired"]

        #gun mags and cooldown
        self.max_mag = weapon_data[self.name]["mag"]
        self.mag = self.max_mag
        self.lastmag = 0
        self.cooldown = 1000
        self.cooldown_bar = CooldownBar((255, 255, 255), self.cooldown, self.name)
        self.on_cooldown = False


    def is_auto(self):
        return weapon_data[self.name]["auto"]
    
    def shoot(self):
        if pygame.time.get_ticks()-self.lastmag > self.cooldown:
            match self.weapon_type:
                case "shotgun":
                        for i in range(self.bullets_fired):
                            ratio = i/(self.bullets_fired-1) #ratio between bullets
                            add_angle = 20 * (2*ratio-1) #angle between bullets
                            bullets.append(Bullet(self.rect.centerx + cos(radians(self.angle)) * self.width/2, 
                                                self.rect.centery - sin(radians(self.angle)) * self.width/2,
                                                weapon_data[self.name]["bullet_type"],
                                                weapon_data[self.name]["bullet_damage"],
                                                self.angle + add_angle, 
                                                weapon_data[self.name]["bullet_speed"], 
                                                weapon_data[self.name]["spread"]))
                        self.mag -= 1
        
        if self.mag <= 0: 
            self.lastmag = pygame.time.get_ticks()
            self.cooldown_bar.last_time =  self.lastmag
            cooldown_bars.append(self.cooldown_bar)
            self.mag = self.max_mag

    def update(self, x, y):
        mouse_pos = pygame.mouse.get_pos()
        self.angle = degrees(atan2(-(mouse_pos[1]/R-y+scroll[1]), mouse_pos[0]/R-x+scroll[0]))

        if self.angle > 90 or self.angle < -90:
            image = pygame.transform.flip(self.image, True, False)
            image = pygame.transform.rotate(image, self.angle + 180)
        else:
            image = pygame.transform.rotate(self.image, self.angle)

        self.rect = image.get_rect(center=(x + cos(radians(self.angle)) * self.rotation[1], y - sin(radians(self.angle)) * self.rotation[0]))
        #pygame.draw.rect(display, (255, 0, 0), self.rect, 2)
        display.blit(image, (self.rect.x-scroll[0], self.rect.y-scroll[1]))


class Bullet:
    def __init__(self, x, y, bullet_type, damage, angle, speed, spread):
        self.bullet_type = bullet_type
        self.angle = angle + uniform(-spread, spread)
        self.image = imgload("assets", "images", f"{self.bullet_type}_bullet.png")
        self.image = pygame.transform.rotate(self.image, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = x, y
        self.vel_x = cos(radians(self.angle)) * speed
        self.vel_y = sin(radians(self.angle)) * speed
        self.damage = damage

    def update(self):
        self.rect.x += self.vel_x
        self.rect.y -= self.vel_y

        for t in basic_map.tiles:
            if t.rect.colliderect(self.rect): 
                if self in bullets:
                    bullets.remove(self)

        if self.rect.centerx-scroll[0] > WIDTH or self.rect.centerx-scroll[0] < 0 or self.rect.centery-scroll[1] > HEIGHT or self.rect.centery-scroll[1] < 0:
            if self in bullets:
                bullets.remove(self)

        #pygame.draw.rect(display, (255, 0, 0), self.rect, 2)
        if self.bullet_type == "default":
            create_bloom(self.image, (20, 20, 15), 2, pygame.Rect(self.rect.x-scroll[0], self.rect.top-scroll[1], self.rect.width, self.rect.height))
        display.blit(self.image, (self.rect.x-scroll[0], self.rect.y-scroll[1]))


class Projectile:
    def __init__(self, x, y, target_x, target_y, damage, aoe):
        self.rect = pygame.Rect(x, y, 15, 15)
        self.damage = damage
        self.gravity = 0.5
        self.aoe = aoe

        d = target_x-x
        self.vel_y = sqrt(2*self.gravity*abs(y-target_y))
        t = self.vel_y / self.gravity
        self.vel_x = d/t/2

        #constant angle to bottom
       #t = sqrt((2*(tan(angle)*abs(d)+abs(y-target_y)))/self.gravity)
        # = d/(t*cos(angle))

        #constant angle to center
        #v = sqrt(abs(d)*self.gravity/sin(2*angle))

        #self.vel_x = v*cos(angle)
        #self.vel_y = abs(v)*sin(angle)

    def update(self):
        self.rect.x += self.vel_x

        self.vel_y -= self.gravity
        self.rect.y -= self.vel_y

        for t in basic_map.tiles:
            if t.rect.colliderect(self.rect): 
                if self in enemy_projectiles:
                    enemy_projectiles.remove(self)


        if self.rect.centerx-scroll[0] > WIDTH or self.rect.centerx-scroll[0] < 0 or self.rect.centery > 396:
            if self in enemy_projectiles:
                enemy_projectiles.remove(self)

        pygame.draw.rect(display, (255, 0, 255), pygame.Rect(self.rect.x-scroll[0], self.rect.top-scroll[1], self.rect.width, self.rect.height))


with open(Path("src", "weapons.toml"), "rb") as f:
    weapon_data = tomllib.load(f)
    weapons = {}
    for k in weapon_data.keys():
        weapons[k] = Weapon(k) 
                        