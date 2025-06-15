import pygame, random, os
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, ENEMY_SPEED, SCALE_FACTOR, ENEMY_MAX_HEALTH

class Enemy(pygame.sprite.Sprite):
    """Wróg z HP i paskiem zdrowia."""
    def __init__(self):
        super().__init__()
        
        # Ustal bazowy katalog względem tego pliku
        base_dir = os.path.dirname(os.path.abspath(__file__))

        # Ścieżka do pliku graficznego wroga
        path = os.path.join(base_dir, "assets","enemy.png")
        img = pygame.image.load(path).convert_alpha()  # Wczytaj grafikę wroga
        w,h = img.get_size()
        # Skalowanie grafiki wroga
        self.image = pygame.transform.scale(img, (w//SCALE_FACTOR, h//SCALE_FACTOR))
        # Losowa pozycja startowa na górze ekranu
        x = random.randint(0, SCREEN_WIDTH-self.image.get_width())
        self.rect = self.image.get_rect(topleft=(x, -self.image.get_height()))
        # Losowy kierunek poziomy (-1, 0, 1)
        self.speed_x = random.choice([-1,0,1])
        self.speed_y = ENEMY_SPEED  # Prędkość pionowa
        self.health = ENEMY_MAX_HEALTH  # Aktualne zdrowie
        self.max_health = ENEMY_MAX_HEALTH  # Maksymalne zdrowie

    def update(self):
        # Ruch wroga po ekranie
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        # Odbicie od krawędzi ekranu
        if self.rect.left<0 or self.rect.right>SCREEN_WIDTH:
            self.speed_x *= -1
        # Jeśli wróg wyleci poza dół ekranu, respawn na górze
        if self.rect.top>SCREEN_HEIGHT:
            self.rect.y = -self.rect.height
            self.rect.x = random.randint(0, SCREEN_WIDTH-self.rect.width)

    def draw(self, surface):
        # Rysowanie wroga na ekranie
        surface.blit(self.image, self.rect)
        # Pasek HP nad wrogiem
        bar_w = self.rect.width
        bar_h = 4
        x,y = self.rect.left, self.rect.top-8
        # Tło paska HP (czerwony)
        pygame.draw.rect(surface, (150,0,0), (x,y,bar_w,bar_h))
        # Aktualny poziom HP (zielony)
        hp_w = int(bar_w * (self.health/self.max_health))
        pygame.draw.rect(surface, (0,255,0), (x,y,hp_w,bar_h))
