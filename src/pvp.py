import os
import pygame
import random
from src.character import create_main_character, load_main_character
from src.utility import load_data
from src.encounter import encounter
from src.menu import main_menu

def generate_random_opponent(characters, player_hero):
    """
    Generate a random opponent from available characters.
    Ensures that the player does not fight against their own hero.
    """
    available_opponents = [char for char in characters if char["class"] != player_hero["class"]]

    if not available_opponents:
        print("Warning: No valid opponent available.")
        return None

    opponent = random.choice(available_opponents)
    return create_main_character(opponent)

def start_pvp(screen):
    """
    Start the PvP mode, allowing the player to battle against a random hero.
    """
    characters = load_data("data/characters.json")

    if not characters:
        print("Error: No characters found in 'characters.json'.")
        return

    # Load existing main character if available
    player_hero = load_main_character()

    if not player_hero:
        print("No main character found. Selecting a hero for PvP...")
        player_hero = select_pvp_hero(screen, characters, "assets/background.jpg")
        if not player_hero:
            print("No hero selected, exiting PvP.")
            return

    print(f"Player is using: {player_hero['class']}")

    # Generate a random opponent (different from player)
    opponent_hero = generate_random_opponent(characters, player_hero)
    if not opponent_hero:
        print("Error: Could not generate an opponent.")
        return

    print(f"Opponent generated: {opponent_hero['class']}")

    # Start PvP encounter
    print("Starting PvP encounter...")
    victory = encounter(screen, player_hero, [opponent_hero], is_pvp=True)

    # Display PvP result with button to return to the main menu


def select_pvp_hero(screen, characters, background_image):
    """
    Allow the player to select their hero for PvP using mouse clicks.
    This function is only called if the player does not already have a hero.
    """
    font = pygame.font.Font(None, 36)
    hero_images = []

    # Load the background
    background = pygame.image.load(background_image)
    background = pygame.transform.scale(background, screen.get_size())

    for char in characters:
        try:
            image = pygame.image.load(char["image"])
            image = pygame.transform.scale(image, (200, 200))
            hero_images.append(image)
        except FileNotFoundError:
            placeholder = pygame.Surface((200, 200))
            placeholder.fill((255, 0, 0))
            hero_images.append(placeholder)

    running = True
    selected_hero = None

    while running:
        screen.blit(background, (0, 0))

        # Dynamic centering
        screen_width, screen_height = screen.get_size()
        items_count = len(characters)
        item_spacing = 300
        total_width = items_count * item_spacing

        # Display instruction text at the top
        instructions = font.render("Click on a hero to choose", True, (255, 255, 255))
        screen.blit(instructions, (screen_width // 2 - instructions.get_width() // 2, 50))

        for idx, char in enumerate(characters):
            x_pos = (screen_width // 2 - total_width // 2) + idx * item_spacing
            y_pos = screen_height // 2 - 100

            screen.blit(hero_images[idx], (x_pos, y_pos))
            class_text = font.render(char["class"], True, (255, 255, 255))
            screen.blit(class_text, (x_pos + 50, y_pos + 210))

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                for idx, char in enumerate(characters):
                    x_pos = (screen_width // 2 - total_width // 2) + idx * item_spacing
                    y_pos = screen_height // 2 - 100
                    if x_pos <= mouse_x <= x_pos + 200 and y_pos <= mouse_y <= y_pos + 200:
                        selected_hero = char
                        running = False

        pygame.display.flip()

    if selected_hero:
        return create_main_character(selected_hero) 
    return None
