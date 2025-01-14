import random
import pygame
from src.effects import apply_effect, random_effect
from src.utility import load_data
from src.merchant import merchant_encounter


encounter_counter = 0


def level_up_animation(screen, font, text):
    """Affiche un texte de niveau gagné qui apparaît et disparaît au milieu de l'écran."""
    clock = pygame.time.Clock()
    alpha = 255
    text_surface = font.render(text, True, (0, 255, 0))
    text_surface.set_alpha(alpha)

    duration = 60  

    for frame in range(duration):
        screen.fill((0, 0, 0))  
        text_surface.set_alpha(alpha)

        
        screen.blit(text_surface, (
            (screen.get_width() - text_surface.get_width()) // 2,
            (screen.get_height() - text_surface.get_height()) // 2
        ))

        pygame.display.flip()
        clock.tick(60)

       
        alpha = max(0, alpha - (255 / duration))


def draw_health_bar(screen, x, y, width, height, current_hp, max_hp, color, border_color):
    """Dessine une barre de santé avec bordures."""
    health_width = max(0, int((current_hp / max_hp) * width))
    pygame.draw.rect(screen, border_color, (x, y, width, height))
    pygame.draw.rect(screen, color, (x, y, health_width, height))


def convert_to_grayscale(image):
    """Convertit une image en niveaux de gris."""
    grayscale = pygame.Surface(image.get_size(), pygame.SRCALPHA)
    grayscale.blit(image, (0, 0))
    arr = pygame.surfarray.array3d(grayscale)
    avg = arr.mean(axis=2, keepdims=True)
    grayscale_arr = avg.repeat(3, axis=2)
    return pygame.surfarray.make_surface(grayscale_arr)


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
    global encounter_counter
    font = pygame.font.Font(None, 36)


    main_character.setdefault('coins', 0)
    main_character.setdefault('status', None)
    main_character.setdefault('max_hp', main_character.get('hp', 100))

    
    selected_monster = random.choices(
        mob_pool,
        weights=[mob["probability"] for mob in mob_pool],
        k=1
    )[0]

    
    try:
        monster_image = pygame.image.load(selected_monster["image"])
        monster_image = pygame.transform.scale(
            monster_image, (min(monster_image.get_width(), 400), min(monster_image.get_height(), 400))
        )
    except FileNotFoundError:
        print(f"Error: Monster image not found ({selected_monster['image']}).")
        monster_image = pygame.Surface((400, 400))
        monster_image.fill((255, 0, 0))

    
    try:
        death_image = pygame.image.load("assets/monsters/death.jpg")
        death_image = pygame.transform.scale(death_image, (400, 400))
    except FileNotFoundError:
        print("Error: Death image not found.")
        death_image = pygame.Surface((400, 400))
        death_image.fill((0, 0, 0))


    enemy = {
        "name": selected_monster["name"],
        "hp": selected_monster["hp"],
        "max_hp": selected_monster["hp"],
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

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  
                    print("Exiting battle...")
                    running = False
                    return False

                if turn == "player" and event.key == pygame.K_a:
                    if main_character["status"] not in ["Frozen", "Stunned"]:
                        effect = random_effect()
                        if effect:
                            apply_effect(enemy, effect)
                        enemy["hp"] -= main_character["attack"]
                        print(f"{main_character['name']} attacked {enemy['name']} for {main_character['attack']} damage!")

                        if enemy["hp"] <= 0:
                            encounter_counter += 1
                            print(f"Encounter count: {encounter_counter}")

                            
                            coins_reward = random.randint(5, 20)
                            main_character["coins"] += coins_reward
                            print(f"You earned {coins_reward} coins! Total coins: {main_character['coins']}")

                            
                            xp_gain = 50
                            main_character.setdefault("xp", 0)
                            main_character.setdefault("level", 1)
                            main_character["xp"] += xp_gain
                            print(f"Gained {xp_gain} XP!")

                            
                            if main_character["xp"] >= main_character["level"] * 100:
                                main_character["level"] += 1
                                main_character["xp"] = 0
                                main_character["max_hp"] += 10  
                                main_character["hp"] = main_character["max_hp"]  
                                print(f"Level up! You are now level {main_character['level']}.")
                                level_up_animation(screen, font, "LEVEL UP!")

                            
                            if encounter_counter % 10 == 0:
                                print("Merchant is appearing!")
                                merchant_encounter(screen, main_character)

                            
                            monster_image = death_image
                            running = False
                            return True
                    else:
                        print(f"{main_character['name']} is unable to act due to {main_character['status']}.")
                    turn = "enemy"

        if turn == "enemy":
            if enemy["status"] not in ["Frozen", "Stunned"]:
                effect = random_effect()
                if effect:
                    apply_effect(main_character, effect)
                main_character["hp"] -= enemy["attack"]
                print(f"{enemy['name']} attacked {main_character['name']} for {enemy['attack']} damage!")

                if main_character["hp"] <= 0:
                    print(f"{main_character['name']} has been defeated by {enemy['name']}.")
                    monster_image = convert_to_grayscale(monster_image)  
                    running = False
                    return False
            else:
                print(f"{enemy['name']} is unable to act due to {enemy['status']}.")
            turn = "player"

        
        screen.fill((0, 0, 0))  
        screen.blit(monster_image, (200, 100))  

        
        draw_health_bar(screen, 50, 450, 300, 20, main_character["hp"], main_character["max_hp"], (255, 0, 0), (255, 255, 255))
        
        draw_health_bar(screen, 450, 100, 300, 20, enemy["hp"], enemy["max_hp"], (0, 255, 0), (255, 255, 255))

        player_coins = main_character.get("coins", 0)
        player_text = font.render(f"{main_character['name']} - Coins: {player_coins}", True, (255, 255, 255))
        screen.blit(player_text, (50, 500))
        pygame.display.flip()

    return False