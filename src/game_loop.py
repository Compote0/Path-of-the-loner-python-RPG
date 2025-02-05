import json
import os
import random
import pygame
from src.encounter import encounter
from src.utility import load_data
from src.class_selection import select_class
from src.equipment_selection import select_equipment

SAVE_FILE = "data/player_save.json"  # save file 

def save_player_data(main_character):
    """Save the player's current state to a file."""
    with open(SAVE_FILE, "w") as file:
        json.dump(main_character, file, indent=4)
    print("Player data saved.")

def load_player_data():
    """Load the player's state from a file if it exists."""
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, "r") as file:
            return json.load(file)
    return None

def generate_rewards():
    """
    Generates random rewards after a battle.
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
    Main game loop for PvE, handling equipment selection, battles, and rewards.
    """
    print("Starting the main PvE game loop.")

    # load player data if exists
    saved_data = load_player_data()
    if saved_data:
        main_character.update(saved_data)  # update maincharacter with data
        print("Loaded saved player data.")

    # Step 1: Load available equipment
    weapons = load_data("data/weapons.json")
    armors = load_data("data/armors.json")
    if not weapons or not armors:
        print("Error: Missing weapons or armors data.")
        return

    # Filter weapons and armors for the selected class
    class_weapons = [weapon for weapon in weapons if weapon["class"] == main_character["class"]]
    class_armors = [armor for armor in armors if armor["class"] == main_character["class"]]

    # verify and select weapon
    if "equipment" not in main_character:
        main_character["equipment"] = {}

    if "weapon" not in main_character["equipment"]:
        print("Prompting weapon selection...")
        selected_weapon = select_equipment(
            screen, class_weapons, "Choose your weapon", background_image="assets/background.jpg"
        )
        if selected_weapon:
            main_character["attack"] += selected_weapon["damage"]
            main_character["equipment"]["weapon"] = selected_weapon
            save_player_data(main_character)  # save after selection
    else:
        print(f"Weapon already selected: {main_character['equipment']['weapon']['name']}")

    # verify and select armor
    if "armor" not in main_character["equipment"]:
        print("Prompting armor selection...")
        selected_armor = select_equipment(
            screen, class_armors, "Choose your armor", background_image="assets/background.jpg"
        )
        if selected_armor:
            main_character["defense"] += selected_armor["defense"]
            main_character["equipment"]["armor"] = selected_armor
            save_player_data(main_character)  # Sauvegarde après sélection
    else:
        print(f"Armor already selected: {main_character['equipment']['armor']['name']}")

    # Step 2: Load monsters and start the game loop
    monsters = load_data("data/monsters.json")
    if not monsters:
        print("Error: No monsters found in 'monsters.json'.")
        return

    for mob in monsters:
        mob["probability"] = 1  # Base probability for all monsters

    current_level = 1  # Initial level

    while main_character["hp"] > 0:
        # Adjust monster probabilities based on the current level
        for mob in monsters:
            if mob["type"] == "Boss":
                mob["probability"] = 0.1 + 0.01 * current_level
            elif mob["type"] == "Elite":
                mob["probability"] = 0.2 + 0.02 * current_level
            else:
                mob["probability"] = 1

        print(f"Starting battle at level {current_level}...")
        victory = encounter(screen, main_character, monsters)

        if not victory:
            print("The hero has fallen. Game over.")
            break

        # Rewards
        rewards = generate_rewards()
        print(f"Rewards obtained: {rewards['gold']} gold and {rewards['items']['name']}.")

        # Apply rewards
        main_character["hp"] = min(main_character["hp"] + rewards["items"].get("healing", 0), main_character["max_hp"])
        if rewards["items"]["type"] == "weapon":
            # verify if the player has a weapon already
            if "weapon" not in main_character["equipment"]:
                main_character["attack"] += rewards["items"]["attack"]
                main_character["equipment"]["weapon"] = rewards["items"]
                save_player_data(main_character)  # save after reward
            else:
                print("You already have a weapon. No new weapon assigned.")

        elif rewards["items"]["type"] == "armor":
            # verify if player has an armor already
            if "armor" not in main_character["equipment"]:
                main_character["defense"] += rewards["items"]["defense"]
                main_character["equipment"]["armor"] = rewards["items"]
                save_player_data(main_character)  # save after reward
            else:
                print("You already have an armor. No new armor assigned.")

        current_level += 1  

    print("Exiting PvE mode.")
