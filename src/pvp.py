import pygame
import random
from src.character import create_main_character
from src.utility import load_data
from src.encounter import encounter

def generate_random_opponent(characters):
    """
    Generate a random opponent from available characters.
    """
    opponent = random.choice(characters)
    return create_main_character(opponent)

def start_pvp(screen):
    """
    Start the PvP mode, allowing the player to battle against a random hero.
    """
    font = pygame.font.Font(None, 36)
    characters = load_data("data/characters.json")

    if not characters:
        print("Error: No characters found in 'characters.json'.")
        return

    # Step 1: Select the hero for the player
    player_hero = select_pvp_hero(screen, characters)
    if not player_hero:
        print("No hero selected, exiting PvP.")
        return

    # Step 2: Generate a random opponent
    opponent_hero = generate_random_opponent(characters)
    print(f"Opponent generated: {opponent_hero['class']}")

    # Step 3: PvP encounter
    print("Starting PvP encounter...")
    victory = encounter(screen, player_hero, [opponent_hero], is_pvp=True)

    if victory:
        print("You won the PvP battle!")
    else:
        print("You lost the PvP battle.")



from src.character import create_main_character, save_main_character  # Ensure save_main_character is imported

def select_pvp_hero(screen, characters):
    """
    Allow the player to select their hero for PvP.
    """
    font = pygame.font.Font(None, 36)
    hero_images = []

    for char in characters:
        try:
            image = pygame.image.load(char["image"])
            image = pygame.transform.scale(image, (150, 150))
            hero_images.append(image)
        except FileNotFoundError:
            placeholder = pygame.Surface((150, 150))
            placeholder.fill((255, 0, 0))
            hero_images.append(placeholder)

    running = True
    selected_hero = None

    while running:
        screen.fill((0, 0, 0))
        for idx, char in enumerate(characters):
            screen.blit(hero_images[idx], (100 + idx * 200, 200))
            class_text = font.render(char["class"], True, (255, 255, 255))
            screen.blit(class_text, (130 + idx * 200, 370))

        instructions = font.render("Press [1], [2], [3], [4] to choose a hero", True, (255, 255, 255))
        screen.blit(instructions, (50, 50))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1 and len(characters) > 0:
                    selected_hero = characters[0]
                elif event.key == pygame.K_2 and len(characters) > 1:
                    selected_hero = characters[1]
                elif event.key == pygame.K_3 and len(characters) > 2:
                    selected_hero = characters[2]
                elif event.key == pygame.K_4 and len(characters) > 3:
                    selected_hero = characters[3]

                if selected_hero:
                    running = False

        pygame.display.flip()

    if selected_hero:
        player_hero = create_main_character(selected_hero)
        save_main_character(player_hero)  # Save the character to a JSON file
        return player_hero
    return None
