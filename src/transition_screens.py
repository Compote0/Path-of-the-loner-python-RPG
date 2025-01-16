import pygame


def display_screen(screen, title, subtitle, background, monster_image=None):
    """
    Displays a generic screen with a title, subtitle, background, and optional monster image.
    """
    font_title = pygame.font.Font(None, 64)
    font_subtitle = pygame.font.Font(None, 32)

    title_surface = font_title.render(title, True, (255, 255, 255))
    subtitle_surface = font_subtitle.render(subtitle, True, (255, 255, 255))

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:  # Wait for the player to press 'Q'
                    running = False

        # Draw background
        screen.blit(background, (0, 0))

        # Draw monster image if provided
        if monster_image:
            monster_rect = monster_image.get_rect()
            monster_rect.center = (screen.get_width() // 2, screen.get_height() // 2 - 100)
            screen.blit(monster_image, monster_rect.topleft)

        # Draw title and subtitle
        screen.blit(title_surface, ((screen.get_width() - title_surface.get_width()) // 2, 50))
        screen.blit(subtitle_surface, ((screen.get_width() - subtitle_surface.get_width()) // 2, 150))

        pygame.display.flip()


def encounter_screen(screen, title, subtitle, background, monster_image=None):
    """
    Displays the encounter screen before a battle.
    """
    display_screen(screen, title, subtitle, background, monster_image)


def victory_screen(screen, title, subtitle, background):
    """
    Displays the victory screen after a battle.
    """
    display_screen(screen, title, subtitle, background)


def defeat_screen(screen, title, subtitle, background):
    """
    Displays the defeat screen if the player loses.
    """
    display_screen(screen, title, subtitle, background)


def merchant_screen(screen, title, subtitle, background):
    """
    Displays the screen when a merchant is encountered.
    """
    display_screen(screen, title, subtitle, background)
