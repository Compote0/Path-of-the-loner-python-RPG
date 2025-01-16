import pygame

def select_equipment(screen, items, prompt):
    """
    Displays a selection screen for equipment (weapons or armor).

    Args:
        screen: Pygame surface for rendering.
        items: List of equipment items to choose from.
        prompt: Message to display for the selection.

    Returns:
        dict: The selected equipment item.
    """
    font = pygame.font.Font(None, 36)
    item_images = []

    for item in items:
        try:
            image = pygame.image.load(item["image"])
            image = pygame.transform.scale(image, (150, 150))
            item_images.append(image)
        except FileNotFoundError:
            placeholder = pygame.Surface((150, 150))
            placeholder.fill((255, 0, 0))
            item_images.append(placeholder)

    running = True
    selected_item = None

    while running:
        screen.fill((0, 0, 0))
        prompt_text = font.render(prompt, True, (255, 255, 255))
        screen.blit(prompt_text, ((800 - prompt_text.get_width()) // 2, 50))

        for idx, item in enumerate(items):
            screen.blit(item_images[idx], (100 + idx * 200, 200))
            item_text = font.render(item["name"], True, (255, 255, 255))
            screen.blit(item_text, (130 + idx * 200, 370))

        instructions = font.render("Press [1], [2], [3], ... to choose an item", True, (255, 255, 255))
        screen.blit(instructions, (50, 500))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                return None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1 and len(items) > 0:
                    selected_item = items[0]
                elif event.key == pygame.K_2 and len(items) > 1:
                    selected_item = items[1]
                elif event.key == pygame.K_3 and len(items) > 2:
                    selected_item = items[2]
                elif event.key == pygame.K_4 and len(items) > 3:
                    selected_item = items[3]

                if selected_item:
                    running = False

        pygame.display.flip()

    return selected_item
