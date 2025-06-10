import pygame
import random
from settings import POWERUP_TYPES, POWERUP_SPEED

class PowerUp(pygame.sprite.Sprite):
    """Spadający bonus – typ: 'health' lub 'homing'."""
    COLOR_MAP = {
        'health': (0, 255, 0),
        'homing': (255, 0, 255)
    }
    def __init__(self, x, y):
        super().__init__()
        self.kind = random.choice(POWERUP_TYPES)
        # rysujemy kółko
        radius = 10
        self.image = pygame.Surface((radius*2, radius*2), pygame.SRCALPHA)
        pygame.draw.circle(self.image,
                           PowerUp.COLOR_MAP[self.kind],
                           (radius, radius),
                           radius)
        self.rect = self.image.get_rect(center=(x, y))
    def update(self):
        """Spada w dół, znika poza ekranem."""
        self.rect.y += POWERUP_SPEED
        if self.rect.top > pygame.display.get_surface().get_height():
            self.kill()
