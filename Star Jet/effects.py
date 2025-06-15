import pygame
import os

class Explosion(pygame.sprite.Sprite):
    """Animacja wybuchu po zniszczeniu wroga."""
    frames_cache = []  # cache klatek, żeby nie ładować za każdym razem

    def __init__(self, x, y):
        super().__init__()
        self.frames = self.load_frames()
        self.current_frame = 0
        self.image = self.frames[self.current_frame]
        self.rect = self.image.get_rect(center=(x, y))
        self.animation_speed = 3  # liczba klatek między zmianą obrazka
        self.counter = 0

    @staticmethod
    def preload_frames():
        """Ładujemy klatki animacji z folderu assets/explosion (cache), niezależnie od katalogu roboczego."""
        if Explosion.frames_cache:
            return Explosion.frames_cache

        # Ustal ścieżkę względem pliku effects.py
        base_dir = os.path.dirname(os.path.abspath(__file__))
        base_path = os.path.join(base_dir, "assets", "explosion")
        frames = []
        for i in range(1, 17):
            path = os.path.join(base_path, f"explosion{i}.png")
            image = pygame.image.load(path).convert_alpha()
            frames.append(image)

        Explosion.frames_cache = frames
        return frames

    def load_frames(self):
        """Zwraca klatki animacji z cache."""
        return Explosion.frames_cache

    def update(self):
        """Zmiana klatki animacji i usunięcie po ostatniej."""
        self.counter += 1
        if self.counter >= self.animation_speed:
            self.counter = 0
            self.current_frame += 1
            if self.current_frame < len(self.frames):
                self.image = self.frames[self.current_frame]
            else:
                self.kill()
