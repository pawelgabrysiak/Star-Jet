import pygame
from settings import *
from bullet import Bullet

class Player:
    def __init__(self):
        self.image = pygame.image.load("assets/player.png")
        self.rect = self.image.get_rect(midbottom=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 20))
        self.bullets = pygame.sprite.Group()
        self.cooldown = 0
        self.laser_sound = pygame.mixer.Sound("assets/Laser heavy duty.wav")

    def update(self, keys):
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= PLAYER_SPEED
        if keys[pygame.K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.x += PLAYER_SPEED
        if keys[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= PLAYER_SPEED
        if keys[pygame.K_DOWN] and self.rect.bottom < SCREEN_HEIGHT:
            self.rect.y += PLAYER_SPEED

        if keys[pygame.K_SPACE] and self.cooldown == 0:
            self.bullets.add(Bullet(self.rect.centerx, self.rect.top))
            self.laser_sound.play()
            self.cooldown = 15
        if self.cooldown > 0:
            self.cooldown -= 1

        self.bullets.update()

    def draw(self, surface):
        surface.blit(self.image, self.rect)
        self.bullets.draw(surface)