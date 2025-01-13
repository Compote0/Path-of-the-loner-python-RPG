import pygame
from src.game import start_game

def main_menu(screen):
    background = pygame.image.load("assets/background.jpg")
    font = pygame.font.Font(None, 36)

    play_button = pygame.image.load("assets/button_play.png")
    play_rect = play_button.get_rect(center=(400, 300))

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_rect.collidepoint(event.pos):
                    start_game(screen)  # Lance le jeu
                    return

        screen.blit(background, (0, 0))
        screen.blit(play_button, play_rect)
        pygame.display.flip()
