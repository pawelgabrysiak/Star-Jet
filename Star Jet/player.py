import pygame, os
from settings import PLAYER_SPEED, SCREEN_WIDTH, SCREEN_HEIGHT, SCALE_FACTOR, PLAYER_MAX_HEALTH
from bullet import Bullet

class Player(pygame.sprite.Sprite):
    """Gracz z HP i możliwością homingu."""
    def __init__(self):
        super().__init__()
        path = os.path.join("assets","images","player.png")
        img = pygame.image.load(path).convert_alpha()
        w,h = img.get_size()
        # skalowanie
        self.image = pygame.transform.scale(img, (w//SCALE_FACTOR, h//SCALE_FACTOR))
        self.rect = self.image.get_rect(midbottom=(SCREEN_WIDTH//2, SCREEN_HEIGHT-20))
        self.bullets = pygame.sprite.Group()
        self.cooldown = 0
        # zdrowie
        self.health = PLAYER_MAX_HEALTH
        self.max_health = PLAYER_MAX_HEALTH
        self.homing = False
        self.homing_ticks = 0
        self.laser_sound = pygame.mixer.Sound(os.path.join("assets","sounds","Laser heavy duty.wav"))

    def update(self, keys):
        if keys[pygame.K_LEFT] and self.rect.left>0:   self.rect.x -= PLAYER_SPEED
        if keys[pygame.K_RIGHT] and self.rect.right<SCREEN_WIDTH: self.rect.x += PLAYER_SPEED
        if keys[pygame.K_UP] and self.rect.top>0:      self.rect.y -= PLAYER_SPEED
        if keys[pygame.K_DOWN] and self.rect.bottom<SCREEN_HEIGHT: self.rect.y += PLAYER_SPEED

        # strzał
        if keys[pygame.K_SPACE] and self.cooldown==0:
            b = Bullet(self.rect.centerx, self.rect.top)
            if self.homing: b.homing = True  # w bullet.py musiałbyś obsłużyć homing
            self.bullets.add(b)
            self.laser_sound.play()
            self.cooldown = 15
        if self.cooldown>0: self.cooldown -=1

        # homing czasowo
        if self.homing:
            self.homing_ticks -=1
            if self.homing_ticks<=0:
                self.homing = False

        self.bullets.update()

    def draw(self, surface):
        # gracz
        surface.blit(self.image, self.rect)
        # pasek HP
        bar_w = self.rect.width
        bar_h = 5
        x,y = self.rect.left, self.rect.top-10
        # tło (czerwony)
        pygame.draw.rect(surface, (150,0,0), (x,y,bar_w,bar_h))
        # zdrowie (zielony)
        hp_w = int(bar_w * (self.health/self.max_health))
        pygame.draw.rect(surface, (0,255,0), (x,y,hp_w,bar_h))
        # pociski
        self.bullets.draw(surface)
