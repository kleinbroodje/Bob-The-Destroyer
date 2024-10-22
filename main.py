from player import *
from weapon import *

font = pygame.font.Font(None, 40)
def main():
    clock = pygame.time.Clock()
    running = True
    while running:
        clock.tick(60)
        display.fill((20, 20, 20))
        for event in pygame.event.get():
            player.process_event(event)

            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False  

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if not player.weapon.is_auto() and not player.rolling:
                        player.weapon.shoot()

        for bullet in bullets:
            bullet.update()
        player.update()
        display.blit(font.render(f"{int(clock.get_fps())}", False, (255, 255, 255)), (10, 10))
        screen.blit(display, (0, 0))
        pygame.display.update()  
    pygame.quit()

main()  
