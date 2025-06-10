import pygame, random, os
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, ENEMY_SPEED, SCALE_FACTOR, ENEMY_MAX_HEALTH

class Enemy(pygame.sprite.Sprite):
    """Wróg z HP i paskiem zdrowia."""
    def __init__(self):
        super().__init__()
        path = os.path.join("assets","images","enemy.png")
        img = pygame.image.load(path).convert_alpha()
        w,h = img.get_size()
        self.image = pygame.transform.scale(img, (w//SCALE_FACTOR, h//SCALE_FACTOR))
        x = random.randint(0, SCREEN_WIDTH-self.image.get_width())
        self.rect = self.image.get_rect(topleft=(x, -self.image.get_height()))
        self.speed_x = random.choice([-1,0,1])
        self.speed_y = ENEMY_SPEED
        self.health = ENEMY_MAX_HEALTH
        self.max_health = ENEMY_MAX_HEALTH

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        if self.rect.left<0 or self.rect.right>SCREEN_WIDTH:
            self.speed_x *= -1
        if self.rect.top>SCREEN_HEIGHT:
            # respawn
            self.rect.y = -self.rect.height
            self.rect.x = random.randint(0, SCREEN_WIDTH-self.rect.width)

    def draw(self, surface):
        # wróg
        surface.blit(self.image, self.rect)
        # pasek HP
        bar_w = self.rect.width
        bar_h = 4
        x,y = self.rect.left, self.rect.top-8
        pygame.draw.rect(surface, (150,0,0), (x,y,bar_w,bar_h))
        hp_w = int(bar_w * (self.health/self.max_health))
        pygame.draw.rect(surface, (0,255,0), (x,y,hp_w,bar_h))
