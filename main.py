import pygame
from src.character import load_main_character
from src.class_selection import select_class
from src.game_loop import game_loop
from src.menu import main_menu

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 800))
    pygame.display.set_caption("Path of the Loner")

    # display main menu 
    main_menu(screen)

    # load or create main character
    main_character = load_main_character()
    if not main_character:
        select_class(screen)  # select class
    else:
        game_loop(screen, main_character)  # main loop

    pygame.quit()

if __name__ == "__main__":
    main()
