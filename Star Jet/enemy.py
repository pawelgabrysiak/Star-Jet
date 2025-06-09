import pygame
import random
from settings import *

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("assets/enemy.png")
        x = random.randint(0, SCREEN_WIDTH - self.image.get_width())
        self.rect = self.image.get_rect(topleft=(x, -50))
        self.speed_x = random.choice([-1, 0, 1])
        self.speed_y = ENEMY_SPEED

    def update(self):
        self.rect.y += self.speed_y
        self.rect.x += self.speed_x

        # Odbicie od krawędzi poziomej
        if self.rect.left < 0 or self.rect.right > SCREEN_WIDTH:
            self.speed_x *= -1

        # Reset pozycji jeśli wróg spadnie poza ekran
        if self.rect.top > SCREEN_HEIGHT:
            self.rect.y = -50
            self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)