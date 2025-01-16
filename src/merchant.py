import pygame
import random
from src.utility import load_data

def merchant_encounter(screen, player):
    """
    Handles the merchant interaction, allowing the player to purchase items and apply their effects.

    Args:
        screen: Pygame display surface.
        player: The player's character dictionary.
    """
    font = pygame.font.Font(None, 36)

    # Load the merchant image
    try:
        merchant_image = pygame.image.load("assets/PNJ/merchant1.jpg")
        merchant_image = pygame.transform.scale(merchant_image, (1920, 1080))
    except FileNotFoundError:
        print("Error: Merchant image not found. Using placeholder.")
        merchant_image = pygame.Surface((1920, 1080))
        merchant_image.fill((50, 50, 50))  # Dark gray placeholder

    # Load merchant items (weapons)
    try:
        merchant_items = load_data("data/weapons.json")
    except FileNotFoundError:
        print("Error: Weapons data file not found!")
        merchant_items = []

    # Select a random weapon
    random_weapon = random.choice(merchant_items) if merchant_items else None

    # Add potions with their effects
    potions = [
        {"name": "Health Potion", "effect": "regen", "value": 10, "damage": 10},
        {"name": "Attack Boost Potion", "effect": "boost", "value": 5, "damage": 15}
    ]

    # Create the merchant's final inventory
    inventory = potions
    if random_weapon:
        inventory.insert(0, random_weapon)

    # Information text
    info_text = font.render("Welcome to the merchant! Choose items to buy or press ESC to exit.", True, (255, 255, 255))
    coins_text = font.render(f"Your coins: {player.get('coins', 0)}", True, (255, 255, 255))

    purchased_items = 0
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                # Handle item purchases
                for i, item in enumerate(inventory):
                    if event.key == pygame.K_1 + i and purchased_items < 2 and player["coins"] >= item["damage"]:
                        player["coins"] -= item["damage"]
                        purchased_items += 1

                        # Apply potion effects
                        if item.get("effect") == "regen":
                            player["hp"] = min(player["hp"] + item["value"], 120)  # Cap HP at 120
                            print(f"{item['name']} used: +{item['value']} HP (current HP: {player['hp']})")
                        elif item.get("effect") == "boost":
                            player["attack"] += item["value"]
                            print(f"{item['name']} used: +{item['value']} Attack (current Attack: {player['attack']})")
                        else:
                            print(f"You bought {item['name']}!")

                if event.key == pygame.K_ESCAPE or purchased_items >= 2:
                    running = False

        # Display elements on the screen
        screen.blit(merchant_image, (0, 0))  # Display merchant image
        screen.blit(info_text, (50, 30))
        coins_text = font.render(f"Your coins: {player['coins']}", True, (255, 255, 255))
        screen.blit(coins_text, (50, 80))

        # Display the merchant's inventory
        for i, item in enumerate(inventory):
            effect = f"({item.get('effect', '')})" if 'effect' in item else ""
            item_text = font.render(f"{i + 1}. {item['name']} - {item['damage']} coins {effect}", True, (255, 255, 255))
            screen.blit(item_text, (50, 130 + i * 40))

        pygame.display.flip()
