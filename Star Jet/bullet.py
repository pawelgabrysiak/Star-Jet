import pygame
from settings import BULLET_SPEED

class Bullet(pygame.sprite.Sprite):
    """Klasa reprezentująca pocisk wystrzeliwany przez gracza."""
    def __init__(self, x, y):
        super().__init__()
        # Tworzymy prostokątny obraz pocisku
        self.image = pygame.Surface((5, 10)) # Szerokość 5, wysokość 10
        self.image.fill((255, 255, 0)) # Kolor żółty
        self.rect = self.image.get_rect(center=(x, y)) # Ustawiamy środek pocisku na podane współrzędne
    def update(self):
        """Aktualizujemy pozycję pocisku i usuwamy, gdy wyjdzie poza ekran."""
        self.rect.y -= BULLET_SPEED
        if self.rect.bottom < 0:
            self.kill()
