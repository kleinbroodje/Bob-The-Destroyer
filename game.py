import pygame
import random
import threading
from settings import *

pygame.init()

class Player:
    def __init__(self, x, y, speed):
        self.x = x
        self.y = y
        self.speed = speed
        self.image = idle_bob
        self.running = running_bob
        self.running_cooldown = running_bob_cooldown
        self.running_frame = running_bob_frame
        self.running_last_update = running_last_update
        self.flip = False
        self.rect = self.image.get_rect(topleft= (self.x, self.y))
        self.offset_x = self.rect.x
        self.jumping = False
        self.touching_ground = False
        self.jump_height = 15
        self.vel_y = 0

    def update(self):
        global gravity
        global jumping
        
        key = pygame.key.get_pressed()
        #key d pressed
        if key[pygame.K_d] == 1:
            self.rect.x += self.speed  
            if jumping == False:
                if current_time - self.running_last_update >= self.running_cooldown:
                    self.running_frame += 1
                    self.running_last_update = current_time
                    if self.running_frame >= len(self.running):
                        self.running_frame = 0

                #runnning animation
                self.image = self.running[self.running_frame]
            self.flip = False
                
        #key a pressed
        elif key[pygame.K_a] == 1:
            self.rect.x -= self.speed
            if jumping == False:
                #cooldown per frame
                if current_time - self.running_last_update >= self.running_cooldown:
                    #next frame
                    self.running_frame += 1
                    #resetting cooldown
                    self.running_last_update = current_time
                    #resetting animation
                    if self.running_frame >= len(self.running):
                        self.running_frame = 0

                #running animation but flipped
                self.image = pygame.transform.flip(self.running[self.running_frame], True, False)
            self.flip = True

        else:
            #idle left or right based on self.flip
            if self.flip == True and jumping == False:
                self.image = pygame.transform.flip(idle_bob, True, False)
            elif jumping == False:
                self.image = idle_bob
            self.running_frame = 0

        self.vel_y -= gravity
        self.rect.y -= self.vel_y

        for t in tile_rects:
            if t.colliderect(self.rect):
                self.rect.bottom = t.top
                jumping = False
                self.vel_y = 0

        if key[pygame.K_w] and not jumping:
            self.vel_y = self.jump_height
            jumping = True
    
        if jumping == True and self.flip == False:
            self.image = jumping_bob

        elif jumping == True and self.flip:
            self.image = pygame.transform.flip(jumping_bob, True, False)   
    

        display.blit(self.image, (self.rect.x - scroll[0], self.rect.y))

#bullet class
class Bullet:
    def __init__(self, type):
        self.image = bullet
        self.flip = player.flip
        #postioning
        if self.flip:
            self.x = player.rect.x - 25
            self.y = player.rect.y + 21
        else:
            self.x = player.rect.x + 43
            self.y = player.rect.y + 21
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        self.rect = self.rect.inflate(-10, 0)
        self.type = type

    def update(self):
        global hp_bar_last_update
        global current_time

        #blitting and moving bullet if type is assault rifle
        if self.type == "ar":
            display.blit(self.image, (self.rect.x - 20 - scroll [0] if self.flip else self.rect.x + 10 - scroll[0], self.rect.y))
            if self.flip:
                self.rect.x -= 15
            else:
                self.rect.x += 15

        #blitting and moving bullet if type is shotgun
        if self.type == "sg1":
            display.blit(self.image, (self.rect.x - 20 - scroll[0] if self.flip else self.rect.x + 10 - scroll[0], self.rect.y - 1))
            if self.flip:
                self.rect.x -= 20
            else:
                self.rect.x += 20
            self.rect.y -= 1.9
        if self.type == "sg2":
            display.blit(self.image, (self.rect.x - 20 - scroll[0] if self.flip else self.rect.x + 10 - scroll[0], self.rect.y - 1))
            if self.flip:
                self.rect.x -= 20
            else:
                self.rect.x += 20
        if self.type == "sg3":
            display.blit(self.image, (self.rect.x - 20 - scroll[0] if self.flip else self.rect.x + 10 - scroll[0], self.rect.y - 1))
            if self.flip:
                self.rect.x -= 20
            else:
                self.rect.x += 20
            self.rect.y += 2.5

        #removing bullet if outside of screen
        if (self.rect.x > screen_width + scroll[0]) or (self.rect.x < 0 + scroll[0]):
            bullets.remove(self)

        for f in frogs:
            if self.rect.colliderect(f.rect):
                f.hp_bar.hp -= 35
                f.show_hp = True
                hp_bar_last_update = current_time
                bullets.remove(self)


#Eyeball class
class Eyeball:
    def __init__(self, x, y):
        self.idle_image = pygame.transform.flip(eye_idle, True, False)
        self.image = self.idle_image
        self.x = x
        self.y = y
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        self.rect.height = 50
        self.rect.width = 50

    def update(self):
        for b in bullets:
            if self.rect.colliderect(b.rect):
                self.damage = True
            if self.damage:
                self.image = self.kill[self.kill_frame]
                if current_time - self.kill_last_update >= self.kill_cooldown:
                    self.kill_frame += 1
                    self.kill_last_update = pygame.time.get_ticks()
                    if self.kill_frame == len(self.kill):
                        #eyeballs.remove(self)
                        break
        display.blit(self.image, (self.rect.x, self.rect.y))
     

class Healthbar:
    def __init__(self, x, y, width, height, max_hp):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.max_hp = max_hp
        self.hp = max_hp
    
    def draw(self):
        ratio = self.hp/self.max_hp
        pygame.draw.rect(display, (255, 0, 0), (self.x - scroll[0], self.y, self.width, self.height))
        pygame.draw.rect(display, (0, 128, 0), (self.x - scroll[0], self.y, self.width * ratio, self.height))  


class Frog:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.idle = frog_idle
        self.image = self.idle
        self.rect = self.idle.get_rect(topleft=(self.x, self.y))
        self.rect = self.rect.inflate(-25, -32)       
        self.kill = frog_explosion
        self.kill_last_update = frog_kill_last_update
        self.kill_frame = frog_kill_frame
        self.croak = frog_croak
        self.croak_frame = frog_croak_frame
        self.croak_last_update = frog_croak_last_update
        self.croak_start = False
        self.croak_sound = False
        self.hp = 100
        self.hp_bar = Healthbar(self.rect.x + 10, self.rect.y - 10, 60, 5, self.hp)
        self.show_hp = False

    def update(self):
        global hp_bar_last_update
        global current_time

        croak = 0
        if croak != 1:
            croak = random.randint(0, 500)

        if croak == 1:
            self.croak_start = True
            self.croak_sound = True

        if self.croak_sound:
            pygame.mixer.Channel(0).play(croak_sound)
            self.croak_sound = False

        if self.croak_start:
            self.image = self.croak[self.croak_frame]
            if current_time - self.croak_last_update >= 70:
                self.croak_frame += 1
                self.croak_last_update = pygame.time.get_ticks()
                if self.croak_frame  == len(self.croak):
                    self.croak_frame = 0
                    self.croak_start = False
                    croak = random.randint(0, 500)

        if self.hp_bar.hp <= 0:
            self.image = self.kill[self.kill_frame]
            if current_time - self.kill_last_update >= 20:
                self.kill_frame += 1
                self.kill_last_update = pygame.time.get_ticks()
                if self.kill_frame == len(self.kill):
                    pygame.mixer.Channel(3).play(death_sound)
                    frogs.remove(self)

        if self.show_hp:
            self.hp_bar.draw() 

        if current_time - hp_bar_last_update >= 1000:  
            self.show_hp = False

        display.blit(self.image, (self.rect.x -15 - scroll[0], self.rect.y - 15))
        

class Platform:
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.color = color
        self.width = width
        self.height = height
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def update(self):
        pass
    def draw(self):
        pygame.draw.rect(display, self.color, ((self.rect.x - scroll[0]), self.rect.y, self.rect.width, self.rect.height))


#bullets
bullets = []
last_bullet = pygame.time.get_ticks()
ar_cooldown = 100
sg_cooldown = 1700

#Frog
frogs = [Frog(200, 463)]

#screenshake
screenshake = 0

gravity = 1
jumping = False

#music
music = False
pause = False

#player
player = Player(player_x, player_y, player_speed)

#levels
frog_forest = Level("platform.csv")

#main loop
clock = pygame.time.Clock()
running = True
while running:
    clock.tick(60)

    display.blit(bg, (0, 0))

    current_time = pygame.time.get_ticks()

    scroll[0] += (player.rect.x - scroll[0] - 326)/10
   
    if not music:
        pygame.mixer.Channel(2).play(bg_music, -1)
        music = True

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False   

            elif event.key == pygame.K_f:
                    if gun == "ar":
                        if current_time - last_bullet >= ar_cooldown:
                            gun = "sg"
                            last_bullet = 0
                    elif gun == "sg":
                        if current_time - last_bullet >= sg_cooldown:
                            gun = "ar" 
                            last_bullet = 0  

            elif event.key == pygame.K_SPACE:
                if gun == "sg":
                    if current_time - last_bullet >= sg_cooldown:
                        bullets.append(Bullet(gun + "1"))
                        bullets.append(Bullet(gun + "2"))
                        bullets.append(Bullet(gun + "3"))
                        pygame.mixer.Channel(1).play(shotgun_sound)
                        last_bullet = current_time
                        screenshake = 20
            
            elif event.key == pygame.K_m:
                if not pause:
                    pygame.mixer.Channel(2).pause()
                    pause = True

                elif pause:
                    pygame.mixer.Channel(2).unpause()
                    pause = False
    
    key = pygame.key.get_pressed()

    #shooting bullets
    if key[pygame.K_SPACE]:
        #cooldown for assault rifle
        if gun == "ar":
            if current_time - last_bullet >= ar_cooldown:
                #adding bullet object to list
                bullets.append(Bullet(gun))
                pygame.mixer.Channel(1).play(gun_sound)
                last_bullet = current_time
                screenshake = 15

    #screenshake 
    if screenshake > 0:
        screenshake -= 1

    render_offset = [0, 0]
    if screenshake:
        render_offset[0] = random.randint(-4, 4) 
        render_offset[1] = random.randint(-4, 4) 

    player.update()

        #guns left and right
    if player.flip and gun == "ar":
        display.blit(pygame.transform.flip(assault_rifle, True, False), (player.rect.x - 20 - scroll[0], player.rect.y + 17))
    elif gun == "ar":
        display.blit(assault_rifle, (player.rect.x - scroll[0], player.rect.y + 17))
    if player.flip and gun == "sg":
        display.blit(pygame.transform.flip(shotgun, True, False), (player.rect.x - 20 - scroll[0], player.rect.y + 22))
    elif gun == "sg":
        display.blit(shotgun, (player.rect.x - scroll[0], player.rect.y + 22))

    frog_forest.update()

    for f in frogs:
        f.update() 

    for b in bullets:
        b.update()
    
    if frogs == []:
        frogs.append(Frog(random.randint(0, 640), 463))

    screen.blit(pygame.transform.scale(display, (screen_width, screen_height)), render_offset) #display is blitted on surface 
    pygame.display.update()

pygame.quit()