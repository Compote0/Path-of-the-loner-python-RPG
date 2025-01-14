import pygame
from src.utility import load_data

def merchant_encounter(screen, player):
    """
    Handles the merchant interaction, allowing the player to purchase items.

    Args:
        screen: Pygame display surface.
        player: The player's character dictionary.
    """
    font = pygame.font.Font(None, 36)
    try:
        background = pygame.image.load("assets/PNJ/merchant.jpg")
        background = pygame.transform.scale(
            background, (min(background.get_width(), 800), min(background.get_height(), 600))
        )
    except FileNotFoundError:
        print("Error: Merchant image not found!")
        return

    
    merchant_items = load_data("data/weapons.json")

    
    if len(merchant_items) < 2:
        print("Error: Not enough items in merchant inventory.")
        return

    info_text = font.render("Welcome to the merchant! Choose 2 items to buy or press ESC to exit.", True, (255, 255, 255))
    coins_text = font.render(f"Your coins: {player.get('coins', 0)}", True, (255, 255, 255))

    purchased_items = 0
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1 and purchased_items < 2 and player["coins"] >= merchant_items[0]["damage"]:
                    player["coins"] -= merchant_items[0]["damage"]
                    purchased_items += 1
                    print(f"You bought {merchant_items[0]['name']}!")
                elif event.key == pygame.K_2 and purchased_items < 2 and player["coins"] >= merchant_items[1]["damage"]:
                    player["coins"] -= merchant_items[1]["damage"]
                    purchased_items += 1
                    print(f"You bought {merchant_items[1]['name']}!")
                elif event.key == pygame.K_ESCAPE or purchased_items >= 2:
                    running = False

       
        screen.fill((0, 0, 0))  
        screen.blit(background, (100, 50)) 
        screen.blit(info_text, (50, 50))
        coins_text = font.render(f"Your coins: {player['coins']}", True, (255, 255, 255))
        screen.blit(coins_text, (50, 100))

        for i, item in enumerate(merchant_items[:2]):  
            item_text = font.render(f"{i + 1}. {item['name']} - {item['damage']} coins", True, (255, 255, 255))
            screen.blit(item_text, (50, 150 + i * 30))

        pygame.display.flip()
