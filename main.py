import pygame
from src.menu import main_menu
from src.game_loop import game_loop
from src.character import load_main_character

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Path of the Loner")

    main_menu(screen)  # Appel au menu principal

    # Une fois l'option sélectionnée
    main_character = load_main_character()
    game_loop(screen, main_character)

    pygame.quit()

if __name__ == "__main__":
    main()
