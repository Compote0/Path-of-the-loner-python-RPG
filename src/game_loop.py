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

def display_rewards(screen, font, rewards):
    """
    Affiche les récompenses gagnées après un combat.
    """
    screen.fill((0, 0, 0))
    reward_text = font.render(
        f"Récompenses : {rewards['gold']} or et {rewards['items']['name']}",
        True,
        (255, 255, 0)
    )
    screen.blit(reward_text, (
        (screen.get_width() - reward_text.get_width()) // 2,
        screen.get_height() // 2
    ))
    pygame.display.flip()
    pygame.time.wait(2000)

def game_loop(screen, main_character):
    """
    Boucle principale du jeu gérant les combats et les récompenses.
    """
    # Vérification de l'initialisation de Pygame
    if not pygame.get_init():
        raise RuntimeError("Pygame n'est pas initialisé. Vérifiez l'appel à pygame.init().")

    # Initialisation de la police
    pygame.font.init()
    font = pygame.font.Font(None, 36)

    # Chargement des monstres
    monsters = load_data("data/monsters.json")
    if not monsters:
        print("Erreur : Aucun monstre trouvé dans 'monsters.json'.")
        return

    # Initialisation des probabilités des monstres
    for mob in monsters:
        mob["probability"] = 1  # Tous les monstres ont la même probabilité de base

    current_level = 1  # Niveau actuel
    running = True

    while running and main_character["hp"] > 0:
        # Gestion des événements (fermeture du jeu, etc.)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                return

        # Ajustement des probabilités des monstres selon le niveau
        for mob in monsters:
            if mob["type"] == "Boss":
                mob["probability"] = 0.1 + 0.01 * current_level
            elif mob["type"] == "Elite":
                mob["probability"] = 0.2 + 0.02 * current_level
            else:
                mob["probability"] = 1

        # Affichage du niveau actuel
        screen.fill((0, 0, 0))
        level_text = font.render(f"Niveau {current_level}", True, (255, 255, 255))
        screen.blit(level_text, (
            (screen.get_width() - level_text.get_width()) // 2,
            screen.get_height() // 2
        ))
        pygame.display.flip()
        pygame.time.wait(1000)

        # Combat
        print(f"Combat au niveau {current_level}...")
        victory = encounter(screen, main_character, monsters)

        if not victory:
            print("Le héros est mort. Fin du jeu.")
            break

        # Récompenses
        rewards = generate_rewards()
        print(f"Récompenses obtenues : {rewards['gold']} or et {rewards['items']['name']}.")

        # Afficher les récompenses sur l'écran
        display_rewards(screen, font, rewards)

        # Appliquer les récompenses
        main_character["coins"] += rewards["gold"]
        main_character["hp"] = min(
            main_character["hp"] + rewards["items"].get("healing", 0),
            main_character["max_hp"]
        )
        if rewards["items"]["type"] == "weapon":
            main_character["attack"] += rewards["items"]["attack"]
        elif rewards["items"]["type"] == "armor":
            main_character["defense"] += rewards["items"]["defense"]

        current_level += 1  # Passer au niveau suivant

        # Afficher les stats du héros dans la console
        print(f"Stats du héros : {main_character}")

    print("Fin de la boucle principale du jeu.")
