from player import *
from enemy import *


for enemy in enemies:
    enemy.assign_player(player)

def main():
    clock = pygame.time.Clock()
    running = True
    while running:
        clock.tick(60)
        display.fill((20, 20, 20))
        ui_display.fill((0, 0, 0))

        scroll[0] += (player.rect.x-scroll[0]-WIDTH/2+player.rect.width/2)/20
        scroll[1] +=(player.rect.y-scroll[1]-HEIGHT/2+player.rect.height/2)/20

        if len(enemies) < 2:
            enemy = Enemy()
            enemy.assign_player(player)
            enemies.append(enemy)

        #input
        for event in pygame.event.get():
            player.process_event(event)

            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False  

        #update      
        basic_map.update()

        cooldown_bar_y = 20
        for cooldown_bar in cooldown_bars:
            cooldown_bar.bar.y = cooldown_bar_y
            cooldown_bar.update(pygame.time.get_ticks())
            cooldown_bar_y += 10

        for bullet in bullets:
            bullet.update()

        for enemy_projectile in enemy_projectiles:
            enemy_projectile.update()

        for enemy in enemies:
            enemy.update()

        player.update()

        #render
        ui_display.blit(font[40].render(f"{int(clock.get_fps())}", False, (255, 255, 255)), (10, 5))
        #ui_display.blit(font[40].render(f"{player.hp}", False, (255, 255, 255)), (((player.rect.x-scroll[0])*R), ((player.rect.y-scroll[1])*R)))

        screen.blit(pygame.transform.scale_by(display, R), (0, 0))
        ui_display.set_colorkey((0, 0, 0))
        screen.blit(ui_display, (0, 0))

        pygame.display.update()  

    pygame.quit()

main()  
