import os
import pygame

def select_class(screen, characters, background_image):
    """
    Allow the player to select their class using mouse clicks.
    """
    font = pygame.font.Font(None, 36)
    class_images = []

    # load and adapt the background to the screen size
    background = pygame.image.load(background_image)
    background = pygame.transform.scale(background, screen.get_size())  

    for char in characters:
        try:
            image = pygame.image.load(char["image"])
            image = pygame.transform.scale(image, (200, 200))
            class_images.append(image)
        except FileNotFoundError:
            placeholder = pygame.Surface((200, 200))
            placeholder.fill((255, 0, 0))
            class_images.append(placeholder)

    running = True
    selected_class = None

    while running:
        screen.blit(background, (0, 0))

        # dynamic centering
        screen_width, screen_height = screen.get_size()
        items_count = len(characters)
        item_spacing = 300
        total_width = items_count * item_spacing

        # center the instruction text above the classes
        instructions = font.render("Click on a class to choose your class", True, (255, 255, 255))
        screen.blit(instructions, (screen_width // 2 - instructions.get_width() // 2, 50))

        for idx, char in enumerate(characters):
            x_pos = (screen_width // 2 - total_width // 2) + idx * item_spacing
            y_pos = screen_height // 2 - 100

            screen.blit(class_images[idx], (x_pos, y_pos))
            class_text = font.render(char["class"], True, (255, 255, 255))
            screen.blit(class_text, (x_pos + 50, y_pos + 210))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                for idx, char in enumerate(characters):
                    x_pos = (screen_width // 2 - total_width // 2) + idx * item_spacing
                    y_pos = screen_height // 2 - 100
                    if x_pos <= mouse_x <= x_pos + 200 and y_pos <= mouse_y <= y_pos + 200:
                        selected_class = char
                        running = False

        pygame.display.flip()
    
    return selected_class
