import random
import pygame
from src.effects import apply_effect, random_effect
from src.utility import load_data
from src.merchant import merchant_encounter

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
    """Dessine une barre de santé esthétique avec bordures et coins arrondis."""
    health_width = max(0, int((current_hp / max_hp) * width))

    # Fond de la barre de vie
    pygame.draw.rect(screen, border_color, (x - 2, y - 2, width + 4, height + 4), border_radius=5)

    # Barre de vie actuelle
    pygame.draw.rect(screen, color, (x, y, health_width, height), border_radius=5)


def show_console(screen, font):
    """Affiche une console en bas à droite avec les logs."""
    console_width = 400
    console_height = 200
    console_x = screen.get_width() - console_width - 20
    console_y = screen.get_height() - console_height - 20

    # Dessiner la console
    pygame.draw.rect(screen, (30, 30, 30), (console_x, console_y, console_width, console_height), border_radius=10)
    pygame.draw.rect(screen, (200, 200, 0), (console_x, console_y, console_width, console_height), 3, border_radius=10)

    # Afficher les logs
    for i, log in enumerate(console_log[-8:]):  # Derniers 8 logs
        text_surface = font.render(log, True, (255, 255, 0))
        screen.blit(text_surface, (console_x + 10, console_y + 10 + i * 20))


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
    global encounter_counter, console_log
    font = pygame.font.Font(None, 24)

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
            monster_image, (screen.get_width() // 3, screen.get_height() // 3)
        )
    except FileNotFoundError:
        print(f"Error: Monster image not found ({selected_monster['image']}).")
        monster_image = pygame.Surface((400, 400))
        monster_image.fill((255, 0, 0))

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
                    print("Exiting game...")
                    running = False
                    return False

                if turn == "player" and event.key == pygame.K_a:
                    if main_character["status"] not in ["Frozen", "Stunned"]:
                        effect = random_effect()
                        if effect:
                            apply_effect(enemy, effect)
                        enemy["hp"] -= main_character["attack"]
                        console_log.append(f"You attacked {enemy['name']} for {main_character['attack']} damage!")

                        if enemy["hp"] <= 0:
                            encounter_counter += 1
                            console_log.append(f"{enemy['name']} defeated!")

                            coins_reward = random.randint(5, 20)
                            main_character["coins"] += coins_reward
                            console_log.append(f"Earned {coins_reward} coins!")

                            xp_gain = 50
                            main_character.setdefault("xp", 0)
                            main_character.setdefault("level", 1)
                            main_character["xp"] += xp_gain
                            console_log.append(f"Gained {xp_gain} XP!")

                            if main_character["xp"] >= main_character["level"] * 100:
                                main_character["level"] += 1
                                main_character["xp"] = 0
                                main_character["max_hp"] += 10
                                main_character["hp"] = main_character["max_hp"]
                                console_log.append(f"Level up! Level {main_character['level']}.")
                                level_up_animation(screen, font, "LEVEL UP!")

                            if encounter_counter % 10 == 0:
                                merchant_encounter(screen, main_character)

                            fade_effect(screen, monster_image)
                            running = False
                            return True
                    turn = "enemy"

        if turn == "enemy":
            if enemy["status"] not in ["Frozen", "Stunned"]:
                effect = random_effect()
                if effect:
                    apply_effect(main_character, effect)
                main_character["hp"] -= enemy["attack"]
                console_log.append(f"{enemy['name']} attacked you for {enemy['attack']} damage!")

                if main_character["hp"] <= 0:
                    console_log.append("You have been defeated!")
                    fade_effect(screen, monster_image)
                    running = False
                    return False
            turn = "player"

        screen.fill((0, 0, 0))
        screen.blit(monster_image, ((screen.get_width() - monster_image.get_width()) // 2, 100))

        draw_health_bar(
            screen, 50, screen.get_height() - 100, 300, 20,
            main_character["hp"], main_character["max_hp"], (255, 0, 0), (255, 255, 255)
        )
        draw_health_bar(
            screen, screen.get_width() - 350, 100, 300, 20,
            enemy["hp"], enemy["max_hp"], (0, 255, 0), (255, 255, 255)
        )

        player_coins = main_character.get("coins", 0)
        player_text = font.render(f"{main_character['name']} - Coins: {player_coins}", True, (255, 255, 255))
        screen.blit(player_text, (50, screen.get_height() - 50))

        show_console(screen, font)

        pygame.display.flip()

    return False