import os
import pygame

def main_menu(screen):
    print("Loading the main menu...")
    clock = pygame.time.Clock()
    screen_width, screen_height = screen.get_size()

    try:
        background_path = os.path.join("assets", "background.jpg")
        background = pygame.image.load(background_path)
        background = pygame.transform.scale(background, (screen_width, screen_height))
        print("Background successfully loaded.")
    except FileNotFoundError:
        print("Background file not found. Using a black background.")
        background = pygame.Surface(screen.get_size())
        background.fill((30, 30, 30))

    try:
        font_path = os.path.join("assets", "fonts", "pixel_font.ttf")
        title_font = pygame.font.Font(font_path, max(50, screen_width // 25))
        button_font = pygame.font.Font(font_path, max(25, screen_width // 50))
        print("Font successfully loaded.")
    except FileNotFoundError:
        print("Font file not found.")
        return "QUIT"

    # Button texts
    title_text = title_font.render("Path Of the Loner", True, (255, 255, 255))
    play_pve_text = button_font.render("Play PVE", True, (255, 255, 255))
    play_pvp_text = button_font.render("Play PVP", True, (255, 255, 255))
    quit_text = button_font.render("Quit", True, (255, 255, 255))

    button_width, button_height = screen_width // 4, screen_height // 12
    button_spacing = screen_height // 50

    center_x = screen_width // 2 - button_width // 2
    center_y = screen_height // 2 - button_height // 2

    play_pve_rect = pygame.Rect(center_x, center_y - button_height - button_spacing, button_width, button_height)
    play_pvp_rect = pygame.Rect(center_x, center_y, button_width, button_height)
    quit_rect = pygame.Rect(center_x, center_y + button_height + button_spacing, button_width, button_height)

    running = True
    while running:
        screen.blit(background, (0, 0))

        # Draw the title
        title_pos = ((screen_width - title_text.get_width()) // 2, screen_height // 10)
        screen.blit(title_text, title_pos)

        # Draw buttons with rounded borders
        pygame.draw.rect(screen, (50, 50, 50), play_pve_rect, border_radius=10)
        pygame.draw.rect(screen, (50, 50, 50), play_pvp_rect, border_radius=10)
        pygame.draw.rect(screen, (50, 50, 50), quit_rect, border_radius=10)

        # Display button texts
        screen.blit(play_pve_text, (play_pve_rect.centerx - play_pve_text.get_width() // 2, play_pve_rect.centery - play_pve_text.get_height() // 2))
        screen.blit(play_pvp_text, (play_pvp_rect.centerx - play_pvp_text.get_width() // 2, play_pvp_rect.centery - play_pvp_text.get_height() // 2))
        screen.blit(quit_text, (quit_rect.centerx - quit_text.get_width() // 2, quit_rect.centery - quit_text.get_height() // 2))

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("Quit event detected.")
                return "QUIT"

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if play_pve_rect.collidepoint(event.pos):
                    print("Play PVE selected.")
                    return "PVE"
                elif play_pvp_rect.collidepoint(event.pos):
                    print("Play PVP selected.")
                    return "PVP"
                elif quit_rect.collidepoint(event.pos):
                    print("Quit selected.")
                    return "QUIT"

        pygame.display.flip()
        clock.tick(60)

    return "QUIT"
