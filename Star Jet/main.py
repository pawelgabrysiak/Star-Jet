import pygame
import os
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS
from game_state import GameState
from ui import FPSCounter

def main():
    """Główna funkcja: inicjalizacja Pygame i pętla gry."""
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Star Jet")

    # Ustawienie ikony okna
    icon_path = os.path.join("assets", "icon.png")
    icon = pygame.image.load(icon_path).convert_alpha()
    pygame.display.set_icon(icon)

    clock = pygame.time.Clock()
    game = GameState(screen)

    # Licznik FPS
    fps_font = pygame.font.SysFont(None, 24)
    fps_counter = FPSCounter(fps_font, position=(SCREEN_WIDTH - 80, 10))

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            game.handle_event(event)

        game.update()
        game.draw()

        # Rysujemy FPS na ekranie
        fps_counter.draw(screen, clock)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
