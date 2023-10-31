import pygame
from csv import reader


pygame.init()

screen_width = 700
screen_height = 700
screen = pygame.display.set_mode((screen_width, screen_height))
display = pygame.Surface((screen_width, screen_height)) 
pygame.display.set_caption("Bob The Destroyer")
scroll = [0, 0]

bg = pygame.image.load("sprites/forest.png")
bg = pygame.transform.scale(bg, (850, 700))

player_x = 0
player_y = 490
player_speed = 6

#spritesheets
player_sheet = pygame.image.load("sprites/Bob_The_Destroyer.png")
guns_sheet = pygame.image.load("sprites/Guns and Ammo.png")
eye_floating_sheet = pygame.image.load("sprites/eye_floating.png")
frog_sheet = pygame.image.load("sprites/Frog.png")

#function for getting frames from spritesheet
def get_image(sheet, frame,  width, height, scale, colorkey):
    image = pygame.Surface((width, height))
    image.blit(sheet, (0, 0), (frame * width, 0, width, height))
    image = pygame.transform.scale(image, (width * scale, height * scale))
    image.set_colorkey(colorkey)
    return image

#Getting single images from sheet
idle_bob = get_image(player_sheet, 0, 12, 14, 4, (0, 0, 0))
jumping_bob = get_image(player_sheet, 7, 12, 14, 4, (0, 0, 0))
assault_rifle = get_image(guns_sheet, 0, 27, 9, 2.5, (0, 0, 0))
shotgun = get_image(guns_sheet, 1, 27, 9, 2.5, (0, 0, 0))
bullet = get_image(guns_sheet, 2, 27, 9, 1, (0, 0, 0))
eye_idle = get_image(eye_floating_sheet, 2, 60, 60, 3, (0, 0, 0))

#Frog animations
frog_animations = []
for f in range(13):
    frog_animations.append(get_image(frog_sheet, f, 106, 102, 1, (0, 0, 0)))

#frog idle and damage
frog_idle = frog_animations[0]
#frog croak
frog_croak = frog_animations[5:7]  + frog_animations[5:6] + frog_animations[0:1]
frog_croak_frame = 0
frog_croak_last_update = 0

#frog explosion animation
frog_explosion = frog_animations[1:5]
frog_kill_frame = 0
frog_kill_last_update = 0

#getting the frames, fps and last_update of the running animation for bob
running_bob = []
running_bob_cooldown = 65
running_bob_frame = 0
running_last_update = 0
for x in range(1, 6):
    running_bob.append(get_image(player_sheet, x, 12, 14, 4, (0, 0, 0)))

#sfx
gun_sound = pygame.mixer.Sound("sfx/arfire.mp3")
shotgun_sound = pygame.mixer.Sound("sfx/shotgun.mp3")
death_sound = pygame.mixer.Sound("sfx/death.mp3")
croak_sound = pygame.mixer.Sound("sfx/croak.mp3")
bg_music = pygame.mixer.Sound("sfx/bg_music.mp3")

#which gun
gun = "ar"

#tiles
tiles_sheet = pygame.image.load("sprites/tiles.png")
tiles = []
tile_size = 32
scale = 1
tile_size = tile_size * scale
for t in range(6):
    tiles.append(get_image(tiles_sheet, t, 32, 32, scale, (0, 0, 0)))
tile_rects = []

def import_csv_layout(path):
    with open(path) as map:
        terrain_map = []
        level = reader(map, delimiter=",")
        for row in level:
            terrain_map.append(list(row))
            
    return terrain_map

class Level:
    def __init__(self, csv):
        self.terrain = import_csv_layout(csv)
        self.tile_x = 0
        self.tile_y = 0

    def update(self):
        self.tile_y = 0
        for row in self.terrain:
            self.tile_x = 0

            for tile in row:
                if tile == "0":
                    display.blit(tiles[0], (self.tile_x * tile_size - scroll[0], self.tile_y * tile_size + player_y + 56))

                if tile == "5":
                    display.blit(tiles[5], (self.tile_x * tile_size - scroll[0],  self.tile_y * tile_size + player_y + 56))

                tile_rects.append(pygame.Rect(self.tile_x * tile_size, self.tile_y * tile_size + player_y + 56, tile_size, tile_size))

                self.tile_x += 1

            self.tile_y += 1





