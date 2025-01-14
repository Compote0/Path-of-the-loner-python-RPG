import pygame
import random
from src.effects import apply_effect
from src.merchant import merchant_encounter


encounter_counter = 0

def encounter(screen, mode):
    """
    Handles a battle encounter between the player and an enemy.
    
    Args:
        screen: Pygame display surface.
        mode: The mode of the encounter (e.g., PVE or PVP).
    """
    global encounter_counter  
    font = pygame.font.Font(None, 36)
    background = pygame.image.load("assets/mob_encounter.jpg")

   
    player = {"name": "Hero", "hp": 100, "attack": 20, "class": "Mage", "status": None, "coins": 20}
    enemy = {"name": "Goblin", "hp": 50, "attack": 10, "class": "Warrior", "status": None}

   
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:  
                    if player["class"] == "Mage":
                        apply_effect(enemy, "frozen")
                    enemy["hp"] -= player["attack"]
                    print(f"{player['name']} attacked {enemy['name']} for {player['attack']} damage!")
                    
                    if enemy["hp"] <= 0:
                        print("You have won!")
                        
                        coins_earned = random.randint(5, 15)
                        player["coins"] += coins_earned
                        print(f"You earned {coins_earned} coins! Total coins: {player['coins']}")

                        
                        encounter_counter += 1
                        print(f"Encounter count: {encounter_counter}")  

                      
                        if encounter_counter % 10 == 0:
                            print("Merchant is appearing!")  
                            merchant_encounter(screen, player)
                        running = False
                elif event.key == pygame.K_ESCAPE:  
                    running = False

        
        screen.blit(background, (0, 0))
        player_text = font.render(f"{player['name']} - HP: {player['hp']} - Coins: {player['coins']} - Status: {player['status']}", True, (255, 255, 255))
        enemy_text = font.render(f"{enemy['name']} - HP: {enemy['hp']} - Status: {enemy['status']}", True, (255, 255, 255))
        screen.blit(player_text, (50, 100))
        screen.blit(enemy_text, (50, 150))

        pygame.display.flip()
