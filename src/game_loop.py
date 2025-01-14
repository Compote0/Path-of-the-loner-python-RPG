import random
from src.encounter import encounter
from src.utility import load_data
import pygame

def generate_rewards():
    """
    Generates random rewards after a battle.
    
    Returns:
        dict: Available rewards.
    """
    rewards = {
        "gold": random.randint(10, 50),
        "items": random.choice([
            {"type": "weapon", "name": "Fire Sword", "attack": 10},
            {"type": "armor", "name": "Scale Armor", "defense": 5},
            {"type": "potion", "name": "Health Potion", "healing": 20}
        ])
    }
    return rewards

def game_loop(screen, main_character):
    """
    Main game loop handling battles and rewards.
    
    Args:
        screen: Pygame display surface.
        main_character: Dictionary representing the hero.
    """
    font = pygame.font.Font(None, 36)

    # Load monsters
    monsters = load_data("data/monsters.json")
    if not monsters:
        print("Error: No monsters found in 'monsters.json'.")
        return

    # Initialize monster probabilities
    for mob in monsters:
        mob["probability"] = 1  # All monsters have equal base probability

    current_level = 1  # Current level or stage

    while main_character["hp"] > 0:
        # Adjust probabilities based on the current level
        for mob in monsters:
            if mob["type"] == "Boss":
                mob["probability"] = 0.1 + 0.01 * current_level  # Bosses appear with low probabilities
            elif mob["type"] == "Elite":
                mob["probability"] = 0.2 + 0.02 * current_level
            else:
                mob["probability"] = 1  # Normal monsters are frequent

        # Battle
        print(f"Battle at level {current_level}...")
        victory = encounter(screen, main_character, monsters)

        if not victory:
            print("The hero has died. Game over.")
            break

        # Rewards
        rewards = generate_rewards()
        print(f"Rewards obtained: {rewards['gold']} gold and {rewards['items']['name']}.")

        # Apply rewards
        main_character["hp"] = min(main_character["hp"] + rewards["items"].get("healing", 0), 100)
        if rewards["items"]["type"] == "weapon":
            main_character["attack"] += rewards["items"]["attack"]
        elif rewards["items"]["type"] == "armor":
            main_character["defense"] += rewards["items"]["defense"]

        current_level += 1  # Move to the next level
