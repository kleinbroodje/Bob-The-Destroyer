from .weapon import *
from .tilemap import *


class Enemy:
    def __init__(self):
        self.last_attack = pygame.time.get_ticks()
        self.gravity = 1
        self.vel_y = 0

    def assign_player(self, player):
        self.player = player

    def update(self):
        self.rect.y -= self.vel_y
        self.vel_y -= self.gravity

        for t in basic_map.tiles:
            if t.rect.colliderect(self.rect): 
                if self.vel_y > 0:
                    self.rect.top = t.rect.bottom
                    self.vel_y = 0

                if self.vel_y < 0:
                    self.rect.bottom = t.rect.top
                    self.vel_y = 0

        for bullet in bullets:
            if self.rect.colliderect(bullet.rect):
                self.hp -= bullet.damage
                bullets.remove(bullet)

        if self.hp <= 0:
            enemies.remove(self)
        

class Slime(Enemy):
    def __init__(self):
        super().__init__()
        self.image = imgload("assets", "images", "blorb.png",)
        self.rect = pygame.Rect(uniform(0, WIDTH-20), 0, 36, 35)
        self.hp = 100
        self.attack_cooldown = 1500
        self.attack_damage = 10

    def attack(self):
        projectile = Projectile(self.rect.centerx, self.rect.centery, self.player.rect.centerx, self.rect.y-100, self.attack_damage, 0)
        enemy_projectiles.append(projectile)
        self.last_attack = pygame.time.get_ticks()

    def update(self):
        super().update()

        if pygame.time.get_ticks() - self.last_attack > self.attack_cooldown:
            self.attack()

        if self.player.rect.x > self.rect.x:
            display.blit(pygame.transform.flip(self.image, True, False), (self.rect.x - 14 - scroll[0], self.rect.y - 13 - scroll[1]))
        else:
            display.blit(self.image, (self.rect.x - 14 - scroll[0], self.rect.y - 13 - scroll[1]))

        #pygame.draw.rect(display, (255, 0, 0), pygame.Rect(self.rect.left - scroll[0], self.rect.top-scroll[1], self.rect.width, self.rect.height), 1)

enemies = [Slime(), Slime()]

