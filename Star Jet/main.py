import pygame
import os
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS
from game_state import GameState
from ui import FPSCounter
from effects import Explosion  # Importujemy klasę Explosion z pliku effects.py

def main():
    """Główna funkcja: inicjalizacja Pygame i pętla gry."""
    pygame.init()  # Inicjalizacja Pygame
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  # Tworzenie okna gry
    pygame.display.set_caption("Star Jet")  # Ustawienie tytułu okna

    # Ustawienie ikony okna (ścieżka względem pliku main.py)
    base_dir = os.path.dirname(os.path.abspath(__file__))
    icon_path = os.path.join(base_dir, "assets", "icon.png")
    icon = pygame.image.load(icon_path).convert_alpha()
    pygame.display.set_icon(icon)

    # PRELOAD klatek wybuchu, aby uniknąć laga przy pierwszym wybuchu
    Explosion.preload_frames()

    # Ładowanie i odtwarzanie muzyki w tle
    music_path = os.path.join(base_dir, "assets", "music.mp3")  # lub .mp3
    pygame.mixer.music.load(music_path)
    pygame.mixer.music.play(-1)  # -1 = zapętlaj

    clock = pygame.time.Clock()  # Zegar do kontroli FPS
    game = GameState(screen)     # Inicjalizacja stanu gry

    # Licznik FPS (czcionka i pozycja)
    fps_font = pygame.font.SysFont(None, 24)
    fps_counter = FPSCounter(fps_font, position=(SCREEN_WIDTH - 80, 10))

    running = True  # Flaga głównej pętli gry
    while running:
        for event in pygame.event.get():  # Obsługa zdarzeń (np. zamknięcie okna)
            if event.type == pygame.QUIT:
                running = False
            game.handle_event(event)

        game.update()  # Aktualizacja stanu gry
        game.draw()    # Rysowanie gry

        # Rysujemy FPS na ekranie
        fps_counter.draw(screen, clock)

        pygame.display.flip()  # Aktualizacja wyświetlacza
        clock.tick(FPS)        # Ograniczenie liczby klatek na sekundę

    pygame.quit()  # Zakończenie działania Pygame

if __name__ == "__main__": # Sprawdzenie czy jest to plik główny
    main()
