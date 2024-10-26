from weapon import *


class Enemy:
    def __init__(self):
        self.rect = pygame.Rect(uniform(0, WIDTH-20), 130, 20, 20)
        self.color = (255, 255, 255)
        self.hp = 100
        self.last_attack = pygame.time.get_ticks()
        self.attack_damage = 10
        self.gravity = 1
        self.vel_y = 0

    def assign_player(self, player):
        self.player = player

    def attack(self):
        projectile = Projectile(self.rect.centerx, self.rect.centery, self.player.rect.centerx, 50, self.attack_damage, 0)
        enemy_projectiles.append(projectile)
        self.last_attack = pygame.time.get_ticks()

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

        self.color = (255, 255, 255)
        for bullet in bullets:
            if self.rect.colliderect(bullet.rect):
                self.color = (255, 0, 0)
                self.hp -= bullet.damage
                bullets.remove(bullet)

        if self.hp <= 0:
            enemies.remove(self)

        if pygame.time.get_ticks() - self.last_attack > 1500:
            self.attack()

        pygame.draw.rect(display, self.color, pygame.Rect(self.rect.x-scroll[0], self.rect.top-scroll[1], self.rect.width, self.rect.height))
        

enemies = [Enemy(), Enemy()]

