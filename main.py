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
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False  

        player.update()
        display.blit(font.render(f"{int(clock.get_fps())}", False, (255, 255, 255)), (10, 10))
        screen.blit(display, (0, 0))
        pygame.display.update()
    pygame.quit()

main()  
