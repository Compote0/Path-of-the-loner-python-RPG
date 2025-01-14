import pygame
from src.effects import apply_effect

def encounter(screen, mode):
    """
    Handles a battle encounter between the player and an enemy.
    
    Args:
        screen: Pygame display surface.
        mode: The mode of the encounter (e.g., PVE or PVP).
    """
    font = pygame.font.Font(None, 36)
    background = pygame.image.load("assets/mob_encounter.jpg")

    # Character creation
    player = {"name": "Hero", "hp": 100, "attack": 20, "class": "Mage", "status": None}
    enemy = {"name": "Goblin", "hp": 50, "attack": 10, "class": "Warrior", "status": None}

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:  # Player attack
                    if player["class"] == "Mage":
                        apply_effect(enemy, "frozen")
                    enemy["hp"] -= player["attack"]
                    if enemy["hp"] <= 0:
                        print("You have won!")
                        running = False
                elif event.key == pygame.K_ESCAPE:  # Quit
                    running = False

        # Display information
        screen.blit(background, (0, 0))
        player_text = font.render(f"{player['name']} - HP: {player['hp']} - Status: {player['status']}", True, (255, 255, 255))
        enemy_text = font.render(f"{enemy['name']} - HP: {enemy['hp']} - Status: {enemy['status']}", True, (255, 255, 255))
        screen.blit(player_text, (50, 100))
        screen.blit(enemy_text, (50, 150))

        pygame.display.flip()
