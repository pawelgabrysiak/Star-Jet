import pygame, os
from settings import PLAYER_SPEED, SCREEN_WIDTH, SCREEN_HEIGHT, SCALE_FACTOR, PLAYER_MAX_HEALTH
from bullet import Bullet

class Player(pygame.sprite.Sprite):
    """Gracz z HP i możliwością homingu."""
    def __init__(self):
        super().__init__()
        
        # Ustal ścieżkę do pliku z grafiką gracza względem tego pliku
        base_dir = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(base_dir, "assets","player.png")
        img = pygame.image.load(path).convert_alpha()  # Wczytaj grafikę gracza
        w,h = img.get_size()
        # Skalowanie grafiki gracza
        self.image = pygame.transform.scale(img, (w//SCALE_FACTOR, h//SCALE_FACTOR))
        # Ustaw pozycję startową gracza na dole ekranu, na środku
        self.rect = self.image.get_rect(midbottom=(SCREEN_WIDTH//2, SCREEN_HEIGHT-20))
        self.bullets = pygame.sprite.Group()  # Grupa pocisków gracza
        self.cooldown = 0  # Cooldown między strzałami
        # Zdrowie gracza
        self.health = PLAYER_MAX_HEALTH
        self.max_health = PLAYER_MAX_HEALTH
        # Tryb homing (pociski samonaprowadzające)
        self.homing = False
        self.homing_ticks = 0  # Licznik czasu trwania homingu
        # Dźwięk strzału
        self.laser_sound = pygame.mixer.Sound(os.path.join(base_dir, "assets","Laser heavy duty.wav"))

    def update(self, keys): # Aktualizacja stanu gracza
        # Ruch gracza po ekranie (strzałki)
        if keys[pygame.K_LEFT] and self.rect.left>0:   self.rect.x -= PLAYER_SPEED
        if keys[pygame.K_RIGHT] and self.rect.right<SCREEN_WIDTH: self.rect.x += PLAYER_SPEED
        if keys[pygame.K_UP] and self.rect.top>0:      self.rect.y -= PLAYER_SPEED
        if keys[pygame.K_DOWN] and self.rect.bottom<SCREEN_HEIGHT: self.rect.y += PLAYER_SPEED

        # Strzał pociskiem po naciśnięciu spacji i jeśli nie ma cooldownu
        if keys[pygame.K_SPACE] and self.cooldown==0:
            b = Bullet(self.rect.centerx, self.rect.top)
            if self.homing: b.homing = True  # Jeśli aktywny homing, ustaw flagę w pocisku
            self.bullets.add(b)
            self.laser_sound.play()  # Odtwórz dźwięk strzału
            self.cooldown = 15  # Ustaw cooldown
        if self.cooldown>0: self.cooldown -=1  # Odliczanie cooldownu

        # Obsługa czasu trwania homingu
        if self.homing:
            self.homing_ticks -=1
            if self.homing_ticks<=0:
                self.homing = False

        self.bullets.update()

    def draw(self, surface): # Rysowanie gracza i jego elementów na ekranie
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
