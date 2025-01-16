import pygame

def main_menu(screen):
    pygame.init()
    clock = pygame.time.Clock()

    # Charger le fond d'écran
    try:
        background = pygame.image.load("assets/background.jpg")
        background = pygame.transform.scale((background), (screen.get_width(), screen.get_height()))
    except FileNotFoundError:
        background = pygame.Surface(screen.get_size())
        background.fill((30, 30, 30))

    # Titre du jeu
    title_font = pygame.font.Font("assets/fonts/pixel_font.ttf", 80)
    title_text = title_font.render("Path of the Loner", True, (255, 255, 255))

    # Boutons
    button_font = pygame.font.Font("assets/fonts/pixel_font.ttf", 40)
    play_text = button_font.render("Play PVE", True, (255, 255, 255))
    pvp_text = button_font.render("Play PVP", True, (255, 255, 255))
    quit_text = button_font.render("Quit", True, (255, 255, 255))

    # Positions des boutons
    button_width, button_height = 300, 80
    button_margin = 20
    play_rect = pygame.Rect(
        (screen.get_width() - button_width) // 2,
        (screen.get_height() // 2) - button_height - button_margin,
        button_width,
        button_height,
    )
    pvp_rect = pygame.Rect(
        (screen.get_width() - button_width) // 2,
        (screen.get_height() // 2),
        button_width,
        button_height,
    )
    quit_rect = pygame.Rect(
        (screen.get_width() - button_width) // 2,
        (screen.get_height() // 2) + button_height + button_margin,
        button_width,
        button_height,
    )

    running = True
    while running:
        screen.blit(background, (0, 0))

        # Afficher le titre
        title_pos = ((screen.get_width() - title_text.get_width()) // 2, 100)
        screen.blit(title_text, title_pos)

        # Dessiner les boutons
        pygame.draw.rect(screen, (50, 50, 50), play_rect, border_radius=10)
        pygame.draw.rect(screen, (50, 50, 50), pvp_rect, border_radius=10)
        pygame.draw.rect(screen, (50, 50, 50), quit_rect, border_radius=10)

        # Texte sur les boutons
        screen.blit(play_text, (play_rect.centerx - play_text.get_width() // 2, play_rect.centery - play_text.get_height() // 2))
        screen.blit(pvp_text, (pvp_rect.centerx - pvp_text.get_width() // 2, pvp_rect.centery - pvp_text.get_height() // 2))
        screen.blit(quit_text, (quit_rect.centerx - quit_text.get_width() // 2, quit_rect.centery - quit_text.get_height() // 2))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if play_rect.collidepoint(event.pos):
                    print("Launching PVE mode...")
                    running = False  # Remplacez par l'appel au mode PVE
                elif pvp_rect.collidepoint(event.pos):
                    print("Launching PVP mode...")
                    running = False  # Remplacez par l'appel au mode PVP
                elif quit_rect.collidepoint(event.pos):
                    running = False

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
