import random
import pygame
from src.encounter import encounter
from src.utility import load_data

def generate_rewards():
    """
    Génère des récompenses aléatoires après un combat.
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
    Boucle principale du mode PVE gérant les combats et les récompenses.
    """
    print("Début de la boucle principale du mode PVE.")

    font = pygame.font.Font(None, 36)

 
    monsters = load_data("data/monsters.json")
    if not monsters:
        print("Erreur : Aucun monstre trouvé dans 'monsters.json'.")
        return

    
    for mob in monsters:
        mob["probability"] = 1  

    current_level = 1  

    while main_character["hp"] > 0:
        
        for mob in monsters:
            if mob["type"] == "Boss":
                mob["probability"] = 0.1 + 0.01 * current_level
            elif mob["type"] == "Elite":
                mob["probability"] = 0.2 + 0.02 * current_level
            else:
                mob["probability"] = 1

  
        print(f"Combat au niveau {current_level}...")
        victory = encounter(screen, main_character, monsters)

        if not victory:
            print("Le héros est mort. Fin du jeu.")
            break

   
        rewards = generate_rewards()
        print(f"Récompenses obtenues : {rewards['gold']} or et {rewards['items']['name']}.")

        
        main_character["hp"] = min(main_character["hp"] + rewards["items"].get("healing", 0), main_character["max_hp"])
        if rewards["items"]["type"] == "weapon":
            main_character["attack"] += rewards["items"]["attack"]
        elif rewards["items"]["type"] == "armor":
            main_character["defense"] += rewards["items"]["defense"]

        current_level += 1  
    print("Fin du mode PVE.")
