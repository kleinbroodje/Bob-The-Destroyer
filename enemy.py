from weapon import *


class Enemy:
    def __init__(self):
        self.rect = pygame.Rect(uniform(0, WIDTH-96), 300, 96, 96)
        self.color = (255, 255, 255)
        self.hp = 100
        self.last_attack = pygame.time.get_ticks()

    def assign_player(self, player):
        self.player = player

    def attack(self):
        projectile = Projectile(self.rect.centerx, self.rect.centery, self.player.rect.centerx, self.player.rect.bottom, radians(65))
        projectiles.append(projectile)
        self.last_attack = pygame.time.get_ticks()

    def update(self):
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

        pygame.draw.rect(display, self.color, self.rect)
        

enemies = [Enemy(), Enemy()]

