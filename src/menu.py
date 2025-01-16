import os
import pygame


def main_menu(screen):
    print("Chargement du menu principal...")
    clock = pygame.time.Clock()

    try:
        background_path = os.path.join("assets", "background.jpg")
        background = pygame.image.load(background_path)
        background = pygame.transform.scale(background, (800, 600))
        print("Fond d'écran chargé avec succès.")
    except FileNotFoundError:
        print("Fichier de fond introuvable. Utilisation d'un fond noir.")
        background = pygame.Surface(screen.get_size())
        background.fill((30, 30, 30))


    try:
        font_path = os.path.join("assets", "fonts", "pixel_font.ttf")
        title_font = pygame.font.Font(font_path, 80)
        button_font = pygame.font.Font(font_path, 40)
        print("Police chargée avec succès.")
    except FileNotFoundError:
        print("Fichier de police introuvable.")
        return "QUIT"

    
    title_text = title_font.render("POTL", True, (255, 255, 255))
    play_pve_text = button_font.render("Play PVE", True, (255, 255, 255))
    quit_text = button_font.render("Quit", True, (255, 255, 255))

    button_width, button_height = 350, 85
    button_spacing = 25

    
    play_pve_rect = pygame.Rect(
        (800 - button_width) // 2,
        (600 // 2) - button_height - button_spacing,
        button_width,
        button_height,
    )
    quit_rect = pygame.Rect(
        (800 - button_width) // 2,
        (600 // 2) + button_spacing,
        button_width,
        button_height,
    )

    running = True
    while running:
        screen.blit(background, (0, 0))

       
        title_pos = ((800 - title_text.get_width()) // 2, 100)
        screen.blit(title_text, title_pos)

        pygame.draw.rect(screen, (50, 50, 50), play_pve_rect, border_radius=10)
        pygame.draw.rect(screen, (50, 50, 50), quit_rect, border_radius=10)
        screen.blit(play_pve_text, (play_pve_rect.centerx - play_pve_text.get_width() // 2, play_pve_rect.centery - play_pve_text.get_height() // 2))
        screen.blit(quit_text, (quit_rect.centerx - quit_text.get_width() // 2, quit_rect.centery - quit_text.get_height() // 2))

        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("Quit event détecté.")
                return "QUIT"

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if play_pve_rect.collidepoint(event.pos):
                    print("Play PVE sélectionné.")
                    return "PVE"
                elif quit_rect.collidepoint(event.pos):
                    print("Quitter sélectionné.")
                    return "QUIT"

        pygame.display.flip()
        clock.tick(60)

    return "QUIT"
