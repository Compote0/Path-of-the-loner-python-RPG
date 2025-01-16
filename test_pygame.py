import pygame

def test_pygame():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Test Pygame")

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((0, 0, 255))
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    test_pygame()
