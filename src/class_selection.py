import pygame
from src.utility import load_data
from src.character import create_main_character, save_main_character
from src.encounter import encounter

def select_class(screen, characters):
    """
    Allow the player to select their class.
    """
    font = pygame.font.Font(None, 36)
    class_images = []

    for char in characters:
        try:
            image = pygame.image.load(char["image"])
            image = pygame.transform.scale(image, (150, 150))
            class_images.append(image)
        except FileNotFoundError:
            placeholder = pygame.Surface((150, 150))
            placeholder.fill((255, 0, 0))
            class_images.append(placeholder)

    running = True
    selected_class = None

    while running:
        screen.fill((0, 0, 0))

        for idx, char in enumerate(characters):
            screen.blit(class_images[idx], (100 + idx * 200, 200))
            class_text = font.render(char["class"], True, (255, 255, 255))
            screen.blit(class_text, (130 + idx * 200, 370))

        instructions = font.render("Press [1], [2], [3], [4] to choose a class", True, (255, 255, 255))
        screen.blit(instructions, (50, 50))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1 and len(characters) > 0:
                    selected_class = characters[0]
                elif event.key == pygame.K_2 and len(characters) > 1:
                    selected_class = characters[1]
                elif event.key == pygame.K_3 and len(characters) > 2:
                    selected_class = characters[2]
                elif event.key == pygame.K_4 and len(characters) > 3:
                    selected_class = characters[3]

                if selected_class:
                    running = False

        pygame.display.flip()

    return selected_class
