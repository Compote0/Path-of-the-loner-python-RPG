import pygame
from src.class_selection import select_class

def main_menu(screen):
    try:
        background = pygame.image.load("assets/background.jpg")
        background = pygame.transform.scale(background, (800, 800))
    except FileNotFoundError:
        background = pygame.Surface((800, 800))
        background.fill((50, 50, 50))

    font = pygame.font.Font(None, 36)

    pve_text = font.render("PVE (Press 1)", True, (255, 255, 255))
    pvp_text = font.render("PVP (Press 2)", True, (255, 255, 255))

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:  # PVE
                    select_class(screen)
                    return
                elif event.key == pygame.K_2:  # PVP
                    print("PVP not implemented yet.")
                    return

        screen.blit(background, (0, 0))
        screen.blit(pve_text, (300, 200))
        screen.blit(pvp_text, (300, 250))
        pygame.display.flip()
