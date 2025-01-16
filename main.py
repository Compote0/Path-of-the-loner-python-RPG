import pygame
from src.menu import main_menu
from src.game_loop import game_loop
from src.character import create_main_character, load_main_character, save_main_character
from src.class_selection import select_class
from src.pvp import start_pvp
from src.utility import load_data

def main():
    try:
        pygame.init()

        screen = pygame.display.set_mode((1920, 1080))
        pygame.display.set_caption("Path of the Loner")

        choice = main_menu(screen)
        print(f"Main menu completed with choice: {choice}")

        if choice == "QUIT":
            print("Exiting the game from the main menu.")
            return

        if choice == "PVP":
            print("Launching PvP mode...")
            start_pvp(screen)
            return

        print("Loading the main character...")
        main_character = load_main_character()
        print(f"Main character loaded: {main_character}")

        if choice == "PVE":
            print("Launching PvE mode...")

            # Load available classes
            characters = load_data("data/characters.json")
            if not characters:
                print("Error: No characters found in 'characters.json'.")
                return

            # Force class selection if no main character exists
            if not main_character:
                print("No main character found. Starting class selection.")
                selected_class = select_class(screen, characters)
                if not selected_class:
                    print("Class selection cancelled. Exiting PvE.")
                    return

                # Create a JSON for the main character after selection
                main_character = create_main_character(selected_class)
                save_main_character(main_character)  # Save the main character

            # Launch the main PvE loop
            game_loop(screen, main_character)

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        print("Closing Pygame.")
        pygame.quit()

if __name__ == "__main__":
    main()
