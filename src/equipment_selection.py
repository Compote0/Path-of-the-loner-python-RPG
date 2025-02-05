import os
import pygame

def select_equipment(screen, items, prompt, background_image, current_selection=None):
    """
    Displays a selection screen for equipment with mouse interactions.
    Prevents overwriting the selection if an item is already equipped.
    """
    # If the player already has selected equipment, return it without re-selection
    if current_selection:
        print(f"{prompt} already selected: {current_selection['name']}")
        return current_selection  

    font = pygame.font.Font(None, 36)
    item_images = []

    # Load and adapt the background to the screen size
    background = pygame.image.load(background_image)
    background = pygame.transform.scale(background, screen.get_size())  

    for item in items:
        try:
            image = pygame.image.load(item["image"])
            image = pygame.transform.scale(image, (200, 200))
            item_images.append(image)
        except FileNotFoundError:
            placeholder = pygame.Surface((200, 200))
            placeholder.fill((255, 0, 0))
            item_images.append(placeholder)

    running = True
    selected_item = None

    while running:
        screen.blit(background, (0, 0))

        # Dynamic centering
        screen_width, screen_height = screen.get_size()
        items_count = len(items)
        item_spacing = 300
        total_width = items_count * item_spacing

        # Center the instruction text above the items
        instructions = font.render(prompt, True, (255, 255, 255))
        screen.blit(instructions, (screen_width // 2 - instructions.get_width() // 2, 50))

        for idx, item in enumerate(items):
            x_pos = (screen_width // 2 - total_width // 2) + idx * item_spacing
            y_pos = screen_height // 2 - 100

            screen.blit(item_images[idx], (x_pos, y_pos))
            item_text = font.render(item["name"], True, (255, 255, 255))
            screen.blit(item_text, (x_pos + 50, y_pos + 210))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                return current_selection  # Keep the current selection if the user exits

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                for idx, item in enumerate(items):
                    x_pos = (screen_width // 2 - total_width // 2) + idx * item_spacing
                    y_pos = screen_height // 2 - 100
                    if x_pos <= mouse_x <= x_pos + 200 and y_pos <= mouse_y <= y_pos + 200:
                        selected_item = item
                        running = False

        pygame.display.flip()
    
    return selected_item if selected_item else current_selection  # Keep previous selection if none chosen
