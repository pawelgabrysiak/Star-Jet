"""star jet/
├── .venv/
├── assets/
│   ├── images/
│   │   └── explosion/
│   │       ├── background.png
│   │       ├── enemy.png
│   │       ├── icon.png
│   │       └── player.png
│   └── sounds/
│       ├── explosion.wav
│       ├── laser.wav
│       └── Laser heavy duty.wav
├── bullet.py
├── effects.py
├── enemy.py
├── game_state.py
├── main.py
├── player.py
├── settings.py
└── ui.py
"""
# ui.py
# Moduł elementów interfejsu użytkownika: przyciski, napisy i licznik FPS.

import pygame

class Button:
    """Przycisk z obsługą hover i kliknięcia."""
    def __init__(self, text, rect, font, bg_color=(0, 200, 0), hover_color=(0, 255, 0), text_color=(0, 0, 0)):
        self.text = text
        self.rect = pygame.Rect(rect)
        self.font = font
        self.bg_color = bg_color
        self.hover_color = hover_color
        self.text_color = text_color

    def draw(self, surface):
        """Rysuje przycisk, zmieniając kolor przy hover."""
        mouse = pygame.mouse.get_pos()
        color = self.hover_color if self.rect.collidepoint(mouse) else self.bg_color
        pygame.draw.rect(surface, color, self.rect)
        label = self.font.render(self.text, True, self.text_color)
        label_rect = label.get_rect(center=self.rect.center)
        surface.blit(label, label_rect)

    def is_clicked(self, event):
        """Zwraca True, jeśli przycisk został kliknięty myszką."""
        return event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos)

class Label:
    """Etykieta tekstowa wyświetlająca dowolny napis."""
    def __init__(self, font, position, text="", color=(255, 255, 255)):
        self.font = font
        self.position = position
        self.text = text
        self.color = color

    def set_text(self, text):
        """Ustawia zawartość etykiety."""
        self.text = text

    def draw(self, surface):
        """Rysuje etykietę na ekranie."""
        if self.text:
            label = self.font.render(self.text, True, self.color)
            surface.blit(label, self.position)

class Scoreboard:
    """Specjalna etykieta do wyświetlania wyniku gry."""
    def __init__(self, font, position=(10, 10), color=(255, 255, 255)):
        self.label = Label(font, position, "", color)

    def draw(self, surface, score):
        """Aktualizuje i rysuje wynik gry."""
        self.label.set_text(f"Wynik: {score}")
        self.label.draw(surface)

class FPSCounter:
    """Licznik klatek na sekundę (FPS) pomocny podczas testów."""
    def __init__(self, font, position=(10, 40), color=(255, 255, 255)):
        self.label = Label(font, position, "", color)

    def draw(self, surface, clock):
        """Aktualizuje i rysuje bieżące FPS."""
        fps = int(clock.get_fps())
        self.label.set_text(f"FPS: {fps}")
        self.label.draw(surface)
