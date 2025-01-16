import pygame
from src.menu import main_menu
from src.game_loop import game_loop
from src.character import load_main_character
from src.class_selection import select_class


def main():
    try:
        print("Initialisation de Pygame...")
        pygame.init()
        print("Pygame initialisé.")

        # Création de la fenêtre
        screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Path of the Loner")
        print("Fenêtre initialisée avec succès.")

        # Lancement du menu principal
        print("Appel du menu principal...")
        choice = main_menu(screen)
        print(f"Menu principal terminé avec le choix : {choice}")

        if choice == "QUIT":
            print("Fermeture du jeu depuis le menu principal.")
            return

        # Chargement du personnage principal
        print("Chargement du personnage principal...")
        main_character = load_main_character()
        print(f"Personnage principal chargé : {main_character}")

        if not main_character:
            print("Aucun personnage principal trouvé, lancement de la sélection de classe.")
            select_class(screen)
        else:
            if choice == "PVE":
                print("Lancement de la boucle principale du jeu.")
                game_loop(screen, main_character)

    except Exception as e:
        print(f"Une erreur est survenue : {e}")

    finally:
        print("Fermeture de Pygame.")
        pygame.quit()


if __name__ == "__main__":
    main()
