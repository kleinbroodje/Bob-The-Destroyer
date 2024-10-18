from weapon import *


class Player:
    def __init__(self):
        self.images = imgload("assets", "bob_spritesheet.png", columns=9)
        self.cape_images = imgload("assets", "cape_spritesheet.png", columns=11)
        self.cape = self.cape_images[0]
        self.cape_cooldown = 1
        self.has_run = False
        self.bop = False
        self.image = self.images[0]
        self.cape_current_frame = 0
        self.current_frame = 0
        self.rect = pygame.Rect(500, 300, 22 * R, 32 * R)
        self.speed = 6
        self.flip = False

        #jumping and stuff
        self.jumping = False
        self.vel_y = 0
        self.mjump = 20
        self.gravity = 1.5
        self.has_jumped = False

        #weapons
        self.weapon = weapons["shotgun"]

    def keys(self):
        keys = pygame.key.get_pressed()
        self.animate_run = False
        if keys[pygame.K_a]:
            self.rect.x -= self.speed
            self.animate_run = True
            self.flip = True
        if keys[pygame.K_d]:
            self.rect.x += self.speed
            if self.animate_run:
                self.animate_run = False
            else:
                self.animate_run = True
            
            self.flip = False
        if keys[pygame.K_w] and not self.jumping:
            self.cape_current_frame = 6
            self.jumping = True
            self.vel_y = self.mjump
    
    def update(self):
        self.keys()

        if self.jumping:
            self.image = self.images[8]
            self.cape = self.cape_images[0]
            self.rect.y -= self.vel_y
            self.vel_y -= self.gravity

            if self.vel_y <= 0:
                if self.cape_current_frame >= 10:
                    self.cape_current_frame = 7
                self.cape = self.cape_images[int(self.cape_current_frame)]
                self.cape_current_frame += 0.25

            if self.rect.y >= 300:
                self.vel_y = 0
                self.jumping = False
                self.has_jumped = True
            

        elif self.animate_run:
            if self.current_frame >= 8:
                self.current_frame = 1
            self.image = self.images[int(self.current_frame)]
            self.current_frame += 0.25

            if self.cape_current_frame >= 7:
                self.cape_current_frame = 2
            self.cape = self.cape_images[int(self.cape_current_frame)]
            self.cape_current_frame += 0.2

            self.has_run = True
        else:
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

        self.bop = False
        if self.image in [self.images[1], self.images[5]]:
            self.bop = True

        if self.flip:
            self.image = pygame.transform.flip(self.image, True, False)
            self.cape = pygame.transform.flip(self.cape, True, False)
        
        if self.bop:
            display.blit(self.cape, (self.rect.x - 20 * R, self.rect.y - 16 * R + R))
        else:
            display.blit(self.cape, (self.rect.x - 20 * R, self.rect.y - 16 * R))

        display.blit(self.image, (self.rect.x - 21 * R, self.rect.y - 16 * R))
        #pygame.draw.rect(display, (255, 0, 0), self.rect, 2)

        self.weapon.update(self.rect.centerx, self.rect.centery)

player = Player()