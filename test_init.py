import pygame

def test_init():
    try:
        pygame.init()
        print("Pygame initialisé avec succès !")
        screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Test Pygame Initialization")
        pygame.display.flip()
        pygame.time.wait(2000)  # Garde la fenêtre ouverte pendant 2 secondes
        pygame.quit()
    except Exception as e:
        print(f"Erreur lors de l'initialisation de Pygame : {e}")

if __name__ == "__main__":
    test_init()
