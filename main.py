import pygame
import json
from tinydb import TinyDB, Query

def load_data(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600), pygame.WINDOWMAXIMIZED)
    pygame.display.set_caption("Path of the Loner")

    # Charger les données
    armors = load_data("data/armors.json")
    weapons = load_data("data/weapons.json")
    monsters = load_data("data/monsters.json")

    background = pygame.image.load("assets/background.jpg")

    font = pygame.font.Font(None, 36)

    welcome_text = font.render("Bienvenue dans Path of the Loner", True, (255, 255, 255))

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

        screen.blit(background, (0, 0))  
        screen.blit(welcome_text, (200, 50))  # Texte d'accueil

        armor_text = font.render(f"Armure: {armors[0]['name']}, Défense: {armors[0]['defense']}", True, (255, 255, 255))
        weapon_text = font.render(f"Arme: {weapons[0]['name']}, Puissance: {weapons[0]['power']}", True, (255, 255, 255))
        screen.blit(armor_text, (50, 200))
        screen.blit(weapon_text, (50, 250))

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
