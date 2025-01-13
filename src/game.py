import pygame
from src.combat import encounter

def start_game(screen):
    font = pygame.font.Font(None, 36)
    background = pygame.image.load("assets/background.jpg")

    pve_text = font.render("PVE (Appuyez sur 1)", True, (255, 255, 255))
    pvp_text = font.render("PVP (Appuyez sur 2)", True, (255, 255, 255))

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:  # PVE
                    encounter(screen, mode="PVE")
                    return
                elif event.key == pygame.K_2:  # PVP
                    encounter(screen, mode="PVP")
                    return

        screen.blit(background, (0, 0))
        screen.blit(pve_text, (300, 200))
        screen.blit(pvp_text, (300, 250))
        pygame.display.flip()
