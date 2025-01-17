import random
import pygame
from src.effects import apply_effect, random_effect
from src.utility import load_data
from src.merchant import merchant_encounter
from src.transition_screens import encounter_screen, victory_screen, defeat_screen

encounter_counter = 0
console_log = []

def fade_effect(screen, image):
    """Applique un effet de fondu sur l'image affichée."""
    clock = pygame.time.Clock()
    fade_surface = pygame.Surface(image.get_size()).convert()
    fade_surface.fill((0, 0, 0))

    for alpha in range(0, 255, 5):
        screen.fill((0, 0, 0))
        screen.blit(image, ((screen.get_width() - image.get_width()) // 2, 100))
        fade_surface.set_alpha(alpha)
        screen.blit(fade_surface, (0, 0))
        pygame.display.flip()
        clock.tick(30)

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

        screen.blit(
            text_surface,
            (
                (screen.get_width() - text_surface.get_width()) // 2,
                (screen.get_height() - text_surface.get_height()) // 2,
            ),
        )

        pygame.display.flip()
        clock.tick(60)

        alpha = max(0, alpha - (255 / duration))

def draw_health_bar(screen, x, y, width, height, current_hp, max_hp, color, border_color):
    """Dessine une barre de santé ésthétique avec bordures et coins arrondis."""
    health_width = max(0, int((current_hp / max_hp) * width))

  
    pygame.draw.rect(screen, border_color, (x - 2, y - 2, width + 4, height + 4), border_radius=5)

    
    pygame.draw.rect(screen, color, (x, y, health_width, height), border_radius=5)

def show_console(screen, font):
    """Affiche une console en bas à droite avec les logs."""
    console_width = 400
    console_height = 200
    console_x = screen.get_width() - console_width - 20
    console_y = screen.get_height() - console_height - 20

   
    pygame.draw.rect(screen, (30, 30, 30), (console_x, console_y, console_width, console_height), border_radius=10)
    pygame.draw.rect(screen, (200, 200, 0), (console_x, console_y, console_width, console_height), 3, border_radius=10)

    
    for i, log in enumerate(console_log[-8:]):  
        text_surface = font.render(log, True, (255, 255, 0))
        screen.blit(text_surface, (console_x + 10, console_y + 10 + i * 20))

def load_background(image_path):
    """Load and scale the background image."""
    try:
        background = pygame.image.load(image_path)
        background = pygame.transform.scale(background, (1920, 1080))
        return background
    except FileNotFoundError:
        print(f"Error: Background image not found at {image_path}. Using default black background.")
        background = pygame.Surface((1920, 1080))
        background.fill((0, 0, 0))
        return background

def encounter(screen, main_character, mob_pool, is_pvp=False):
    """
    Handles a battle between the hero and a monster or another hero.
    """
    global encounter_counter, console_log
    font = pygame.font.Font(None, 24)
    instruction_font = pygame.font.Font(None, 32)

    main_character.setdefault('coins', 0)
    main_character.setdefault('status', None)
    main_character.setdefault('max_hp', main_character.get('hp', 100))
    
    encounter_counter += 1
    if encounter_counter % 5 == 0:  
        print("Rencontre avec le marchand déclenchée !")
        merchant_encounter(screen, main_character)
        return True  

    if not mob_pool:
        raise ValueError("mob_pool is empty. No opponents available.")

    selected_opponent = random.choice(mob_pool)

    # Debug: Log full data of the opponent
    print(f"Selected opponent data: {selected_opponent}")

    # Use 'type' instead of 'class' for monsters
    opponent_type = selected_opponent.get("type", "Unknown")
    opponent_name = selected_opponent.get("name", "Unknown")
    print(f"Selected opponent: {opponent_name} ({opponent_type})")

    # Load the background
    background_path = selected_opponent.get("background", "assets/monsters_rooms/default_room.jpg")
    try:
        background = load_background(background_path)
    except Exception as e:
        print(f"Error loading background: {e}")
        background = load_background("assets/monsters_rooms/default_room.jpg")

    # Load the opponent's image
    try:
        monster_image = pygame.image.load(selected_opponent["image"])
        scaled_width = monster_image.get_width() // 3
        scaled_height = monster_image.get_height() // 3
        monster_image = pygame.transform.scale(monster_image, (scaled_width, scaled_height))
        monster_rect = monster_image.get_rect()
        monster_rect.center = (screen.get_width() // 2, screen.get_height() // 2 - 100)
    except FileNotFoundError:
        print(f"Error: Opponent image not found ({selected_opponent['image']}).")
        monster_image = pygame.Surface((400, 400))
        monster_image.fill((255, 0, 0))
        monster_rect = monster_image.get_rect()
        monster_rect.center = (screen.get_width() // 2, screen.get_height() // 2 - 100)

    # Enemy data
    enemy = {
        "name": opponent_name,
        "hp": selected_opponent.get("hp", 100),
        "max_hp": selected_opponent.get("hp", 100),
        "attack": selected_opponent.get("attack", 10),
        "type": opponent_type,
        "status": None
    }

    # Screens for victory, encounter, and merchant
    encounter_screen(screen, f"You encountered a {enemy['type']}: {enemy['name']}!", "Press Q to start the battle", background, monster_image)

    # Combat loop
    running = True
    turn = "player"
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    print("Exiting game...")
                    running = False
                    return False
                if turn == "player" and event.key == pygame.K_a:
                    if main_character["status"] not in ["Frozen", "Stunned"]:
                        enemy["hp"] -= main_character["attack"]
                        console_log.append(f"You attacked {enemy['name']} for {main_character['attack']} damage!")
                        if enemy["hp"] <= 0:
                            console_log.append(f"{enemy['name']} defeated!")
                            coins_reward = random.randint(5, 20)
                            main_character["coins"] += coins_reward
                            console_log.append(f"Earned {coins_reward} coins!")
                            victory_screen(screen, f"You defeated {enemy['name']}!", "Press Q to continue your adventure", background)
                            running = False
                            return True
                    turn = "enemy"
        if turn == "enemy":
            main_character["hp"] -= enemy["attack"]
            console_log.append(f"{enemy['name']} attacked you for {enemy['attack']} damage!")
            if main_character["hp"] <= 0:
                console_log.append("You have been defeated!")
                defeat_screen(screen, f"{enemy['name']} has defeated you!", "Press Q to exit", background)
                running = False
                return False
            turn = "player"

        # Draw the background
        screen.blit(background, (0, 0))

        # Draw the opponent image
        screen.blit(monster_image, monster_rect.topleft)

        # Draw health bars with numerical values for the player
        draw_health_bar(
            screen, 50, screen.get_height() - 100, 300, 20,
            main_character["hp"], main_character["max_hp"], (255, 0, 0), (255, 255, 255)
        )
        player_hp_text = font.render(f"{main_character['hp']}/{main_character['max_hp']}", True, (255, 255, 255))
        screen.blit(player_hp_text, (50 + 150 - player_hp_text.get_width() // 2, screen.get_height() - 120))

        # Draw health bars with numerical values for the enemy
        draw_health_bar(
            screen, screen.get_width() - 350, 100, 300, 20,
            enemy["hp"], enemy["max_hp"], (0, 255, 0), (255, 255, 255)
        )
        enemy_hp_text = font.render(f"{enemy['hp']}/{enemy['max_hp']}", True, (255, 255, 255))
        screen.blit(enemy_hp_text, (screen.get_width() - 350 + 150 - enemy_hp_text.get_width() // 2, 80))

        # Draw "Press A to attack" instruction
        instruction_text = instruction_font.render("Press A to attack", True, (255, 255, 255))
        screen.blit(instruction_text, ((screen.get_width() - instruction_text.get_width()) // 2, screen.get_height() - 150))

        # Draw player stats (e.g., coins)
        player_coins = main_character.get("coins", 0)
        player_text = font.render(f"{main_character['name']} - Coins: {player_coins}", True, (255, 255, 255))
        screen.blit(player_text, (50, screen.get_height() - 50))

        # Display console logs
        show_console(screen, font)

        # Update the screen
        pygame.display.flip()

    return False