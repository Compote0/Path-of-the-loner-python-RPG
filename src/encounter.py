import random
import pygame
from src.effects import apply_effect, random_effect
from src.utility import load_data

def encounter(screen, main_character, mob_pool):
    """
    Handles a battle between the hero and a monster.
    
    Args:
        screen: Pygame display surface.
        main_character: Dictionary representing the hero.
        mob_pool: List of available monsters.
        
    Returns:
        bool: True if the hero wins, False if they lose.
    """
    font = pygame.font.Font(None, 36)
    selected_monster = random.choices(
        mob_pool,
        weights=[mob["probability"] for mob in mob_pool],
        k=1
    )[0]

    try:
        monster_image = pygame.image.load(selected_monster["image"])
        monster_image = pygame.transform.scale(monster_image, (800, 600))
    except FileNotFoundError:
        print(f"Error: Monster image not found ({selected_monster['image']}).")
        monster_image = pygame.Surface((800, 600))
        monster_image.fill((255, 0, 0))

    enemy = {
        "name": selected_monster["name"],
        "hp": selected_monster["hp"],
        "attack": selected_monster["attack"],
        "class": selected_monster["type"],
        "status": None
    }

    running = True
    turn = "player"

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                return False

            if event.type == pygame.KEYDOWN and turn == "player":
                if event.key == pygame.K_a:
                    if main_character["status"] not in ["Frozen", "Stunned"]:
                        effect = random_effect()
                        if effect:
                            apply_effect(enemy, effect)
                        enemy["hp"] -= main_character["attack"]
                        if enemy["hp"] <= 0:
                            running = False
                            return True  # The hero wins
                    turn = "enemy"

        if turn == "enemy":
            if enemy["status"] not in ["Frozen", "Stunned"]:
                effect = random_effect()
                if effect:
                    apply_effect(main_character, effect)
                main_character["hp"] -= enemy["attack"]
                if main_character["hp"] <= 0:
                    running = False
                    return False  # The hero loses
            turn = "player"

        screen.blit(monster_image, (0, 0))
        player_text = font.render(f"{main_character['name']} - HP: {main_character['hp']}", True, (255, 255, 255))
        enemy_text = font.render(f"{enemy['name']} - HP: {enemy['hp']}", True, (255, 255, 255))
        screen.blit(player_text, (50, 400))
        screen.blit(enemy_text, (50, 450))
        pygame.display.flip()
