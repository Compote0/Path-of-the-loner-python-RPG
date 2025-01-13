import pygame
import json

def load_data(file_path):
    """
    Charge les données JSON depuis un fichier et gère les erreurs.
    """
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Erreur : Le fichier {file_path} est introuvable.")
        pygame.quit()
        exit()
    except json.JSONDecodeError:
        print(f"Erreur : Le fichier {file_path} contient une erreur et ne peut pas être chargé.")
        pygame.quit()
        exit()

def load_image(file_path):
    """
    Charge une image avec gestion des erreurs.
    """
    try:
        return pygame.image.load(file_path)
    except FileNotFoundError:
        print(f"Erreur : Le fichier {file_path} est introuvable.")
        pygame.quit()
        exit()

class Character:
    """
    Classe représentant un personnage avec des points de vie et une capacité d'attaque.
    """
    def __init__(self, name, hp, attack):
        self.name = name
        self.hp = hp
        self.attack = attack

    def attack_enemy(self, enemy):
        """
        Inflige des dégâts à un ennemi.
        """
        damage = self.attack
        enemy.hp -= damage
        enemy.hp = max(0, enemy.hp)  
        return damage

def main():
    pygame.init()

    
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Path of the Loner")

    
    armors = load_data("data/armors.json")
    weapons = load_data("data/weapons.json")
    monsters = load_data("data/monsters.json")

    if not armors or not weapons or not monsters:
        print("Erreur : Les fichiers JSON sont vides ou invalides.")
        pygame.quit()
        exit()

    
    background = load_image("assets/background.jpg")
    font = pygame.font.Font(None, 36)


    player = Character("Hero", 100, 15)
    monster_data = monsters[0]
    monster = Character(monster_data['name'], monster_data['hp'], monster_data['attack'])

    
    welcome_text = font.render("Bienvenue dans Path of the Loner", True, (255, 255, 255))
    attack_text = font.render("Appuyez sur [A] pour attaquer, [Q] pour quitter", True, (255, 255, 255))

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_ESCAPE, pygame.K_q]:
                    running = False
                elif event.key == pygame.K_a:  
                    damage = player.attack_enemy(monster)
                    print(f"{player.name} attaque {monster.name} pour {damage} dégâts.")
                    if monster.hp <= 0:
                        print(f"{monster.name} est vaincu !")
                        running = False

        
        screen.blit(background, (0, 0))
        screen.blit(welcome_text, (200, 50))
        screen.blit(attack_text, (50, 500))


        player_stats = font.render(f"{player.name} - HP: {player.hp}", True, (255, 255, 255))
        monster_stats = font.render(f"{monster.name} - HP: {monster.hp}", True, (255, 255, 255))
        screen.blit(player_stats, (50, 100))
        screen.blit(monster_stats, (50, 150))

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
