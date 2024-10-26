from weapon import *


class Player:
    def __init__(self):
        self.rect = pygame.Rect(100, 120, 22, 32)
        self.hp = 100

        #player animation
        self.images = imgload("assets", "bob_spritesheet.png", columns=15)
        self.image = self.images[0]
        self.current_frame = 0
        self.flip = False
        self.bop = False

        #cape animation
        self.cape_images = imgload("assets", "cape_spritesheet.png", columns=16)
        self.cape = self.cape_images[0]
        self.cape_current_frame = 0
        self.cape_cooldown = 1

        #running
        self.has_run = False
        self.speed = 3

        #jumping and stuff
        self.jumping = False
        self.vel_y = 0
        self.mjump = 8
        self.gravity = 0.5
        self.has_jumped = False

        #weapons
        self.weapon = weapons["shotgun"]

        #rolling
        self.rolling = False
        self.roll_speed = 4
        self.last_roll = 0
        self.roll_cooldown = 1000
        self.roll_cooldown_bar = CooldownBar((255, 255, 255), self.roll_cooldown, "dodge")

    def keys(self):
        keys = pygame.key.get_pressed()
        self.running = False
        if not self.rolling:
            if keys[pygame.K_a]:
                self.rect.x -= self.speed
                self.running = True
                self.flip = True
            if keys[pygame.K_d]:
                self.rect.x += self.speed

                #added this so you can't run in place
                if self.running:
                    self.running = False
                else:
                    self.running = True
                
                self.flip = False
            if keys[pygame.K_w] and not self.jumping:
                self.cape_current_frame = 6
                self.jumping = True
                self.vel_y = self.mjump
            
    def process_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not (self.jumping or self.rolling) and pygame.time.get_ticks()-self.last_roll > self.roll_cooldown:
                self.last_roll = pygame.time.get_ticks()
                self.roll_cooldown_bar.last_time = self.last_roll
                cooldown_bars.append(self.roll_cooldown_bar)
                self.current_frame = 9
                self.cape_current_frame = 10
                self.has_run = False
                self.rolling = True

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if not self.weapon.is_auto() and not player.rolling:
                    self.weapon.shoot()

    def idle_animation(self):
        self.current_frame = 1
        self.image = self.images[0]
        
        if self.has_run or self.has_jumped:
            if self.cape_cooldown <= 0:
                self.has_run = False
                self.has_jumped = False
                self.cape_current_frame = 1
                self.cape_cooldown = 1
            self.cape = self.cape_images[1]
            self.cape_cooldown -= 0.45
        else:
            self.cape = self.cape_images[0]

    def jump_animation(self):
        self.image = self.images[8]
        self.cape = self.cape_images[0]

        if self.vel_y <= 0:
            if self.cape_current_frame >= 10:
                self.cape_current_frame = 7
            self.cape = self.cape_images[int(self.cape_current_frame)]
            self.cape_current_frame += 0.25

    def rolling_animation(self):
        self.image = self.images[int(self.current_frame)]
        self.current_frame += 0.2

        self.cape = self.cape_images[int(self.cape_current_frame)]
        self.cape_current_frame += 0.2

        if self.current_frame >= 15 and self.cape_current_frame >= 16:
            self.rolling = False 

    def run_animation(self):
        if self.current_frame >= 8:
            self.current_frame = 1
        self.image = self.images[int(self.current_frame)]
        self.current_frame += 0.25

        if self.cape_current_frame >= 7:
            self.cape_current_frame = 2
        self.cape = self.cape_images[int(self.cape_current_frame)]
        self.cape_current_frame += 0.2
            

    def update(self):
        self.keys()

        for enemy_projectile in enemy_projectiles:
            if not self.rolling:
                if self.rect.colliderect(enemy_projectile.rect):
                    self.hp -= enemy_projectile.damage
                    enemy_projectiles.remove(enemy_projectile)

        if self.jumping:
            self.rect.y -= self.vel_y
            self.vel_y -= self.gravity

            self.jump_animation()

            if self.rect.y >= 120:
                self.vel_y = 0
                self.jumping = False
                self.has_jumped = True

        elif self.rolling:
            if self.flip:
                self.rect.x -= self.roll_speed
            else:
                self.rect.x += self.roll_speed

            self.rolling_animation()

        elif self.running:
            self.run_animation()
            self.has_run = True
        
        #when idle or transitioning to idle
        else:
            self.idle_animation()

        self.bop = False
        if self.image in [self.images[1], self.images[5]]:
            self.bop = True

        if self.flip:
            self.image = pygame.transform.flip(self.image, True, False)
            self.cape = pygame.transform.flip(self.cape, True, False)
        
        #lower cape by R pixels when bopping
        if self.bop:
            display.blit(self.cape, ((self.rect.x - 21)-scroll[0], (self.rect.y - 17)-scroll[1]))
        else:
            display.blit(self.cape, ((self.rect.x - 21)-scroll[0], (self.rect.y - 16)-scroll[1]))

        display.blit(self.image, ((self.rect.x - 21)-scroll[0], (self.rect.y - 16)-scroll[1]))
        #pygame.draw.rect(display, (255, 0, 0), self.rect, 2)

        if not player.rolling:
            self.weapon.update(self.rect.centerx, self.rect.centery)


player = Player()