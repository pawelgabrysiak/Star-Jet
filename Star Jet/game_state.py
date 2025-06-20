import pygame, random, os
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, BONUS_SPAWN_TICKS
from player import Player
from enemy import Enemy
from effects import Explosion
from bonus import PowerUp
from ui import Button, Scoreboard

class GameState:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont(None,36)

        # Ustal ścieżki do zasobów względem tego pliku
        base_dir = os.path.dirname(os.path.abspath(__file__))
        bg_path = os.path.join(base_dir, "assets", "background.png")
        explosion_sound_path = os.path.join(base_dir, "assets", "explosion_sound.wav")

        # Wczytaj tło i dźwięk wybuchu
        self.background = pygame.image.load(bg_path).convert()
        self.explosion_sound = pygame.mixer.Sound(explosion_sound_path)

        # Utwórz przycisk "GRAJ" i licznik punktów
        r = pygame.Rect((SCREEN_WIDTH-200)//2,(SCREEN_HEIGHT-60)//2,200,60)
        self.play_button = Button("GRAJ", r, self.font)
        self.scoreboard = Scoreboard(self.font,(10,10))

        self.reset_game()         # Ustaw stan początkowy gry
        self.game_active = False  # Czy gra jest aktywna
        self.game_over = False    # Czy gra się skończyła
        self.game_over_time = 0   # Czas zakończenia gry

        # Grupa bonusów i timer do ich pojawiania się
        self.bonus_group = pygame.sprite.Group()
        self.bonus_timer = 0

    def reset_game(self):
        """Resetuje stan gry do początkowego."""
        self.player      = Player()
        self.enemy_group = pygame.sprite.Group(Enemy() for _ in range(5))  # Startowa liczba wrogów
        self.effects     = pygame.sprite.Group()  # Grupa efektów (np. wybuchy)
        self.score       = 0
        self.milestones  = [10,20,40,60,100]     # Progi punktowe na zwiększenie trudności
        self.added       = [5,10,15,20,25]       # Liczba wrogów dodawanych po osiągnięciu progu
        self.idx         = 0                     # Indeks aktualnego progu
        self.spawn_t     = 0                     # Timer spawnu wrogów
        self.game_over   = False
        self.player.health = self.player.max_health  # Reset zdrowia gracza
        for e in self.enemy_group: e.health = e.max_health  # Reset zdrowia wrogów

    def handle_event(self,event):
        """Obsługuje zdarzenia (np. kliknięcia, restart gry)."""
        if not self.game_active:
            if self.play_button.is_clicked(event):
                self.game_active = True
                self.reset_game()
        elif self.game_over:
            if pygame.time.get_ticks()-self.game_over_time>2000:
                rect = self.play_button.rect
                rect.top = SCREEN_HEIGHT//2+80
                if self.play_button.is_clicked(event):
                    self.game_active=True
                    self.reset_game()

    def update(self):
        """Aktualizuje stan gry (ruchy, kolizje, efekty, bonusy)."""
        if not self.game_active or self.game_over: return

        keys = pygame.key.get_pressed()
        self.player.update(keys)
        self.enemy_group.update()
        self.effects.update()
        self.bonus_group.update()

        # Kolizje: pociski gracza ↔ wrogowie
        hits = pygame.sprite.groupcollide(self.player.bullets, self.enemy_group, True, False)
        for bullet, enemies in hits.items():
            for enemy in enemies:
                enemy.health -=1
                if enemy.health<=0:
                    self.effects.add(Explosion(enemy.rect.centerx,enemy.rect.centery))  # Dodaj animację wybuchu
                    self.explosion_sound.play()  # Odtwórz dźwięk wybuchu
                    enemy.kill()
                    self.score+=1

        # Kolizje: bonusy ↔ gracz
        coups = pygame.sprite.spritecollide(self.player, self.bonus_group, True)
        for b in coups:
            if b.kind=='health':
                self.player.health = min(self.player.max_health, self.player.health+1)  # Leczenie
            elif b.kind=='homing':
                self.player.homing = True
                self.player.homing_ticks = FPS*5  # 5 sekund homingu

        # Sprawdzanie progów punktowych i zwiększanie liczby wrogów
        if self.idx<len(self.milestones) and self.score>=self.milestones[self.idx]:
            for _ in range(self.added[self.idx]):
                self.enemy_group.add(Enemy())
            self.idx+=1

        # Kolizje: gracz ↔ wróg
        if pygame.sprite.spritecollideany(self.player, self.enemy_group):
            self.game_over = True
            self.game_over_time = pygame.time.get_ticks()

        # Okresowy spawn wroga
        self.spawn_t+=1
        if self.spawn_t>=FPS*2:
            self.enemy_group.add(Enemy())
            self.spawn_t=0

        # Okresowy spawn bonusu
        self.bonus_timer+=1
        if self.bonus_timer>=BONUS_SPAWN_TICKS:
            x = random.randint(20, SCREEN_WIDTH-20)
            self.bonus_group.add(PowerUp(x, -10))
            self.bonus_timer=0

    def draw(self):
        self.screen.blit(self.background,(0,0))

        if not self.game_active:
            self.play_button.draw(self.screen)
        elif not self.game_over:
            self.player.draw(self.screen)
            # wróg przez draw()
            for e in self.enemy_group: e.draw(self.screen)
            self.effects.draw(self.screen)
            # bonusy
            self.bonus_group.draw(self.screen)
            self.scoreboard.draw(self.screen, self.score)
        else:
            txt = self.font.render("KONIEC GRY",True,(255,0,0))
            fs  = self.font.render(f"Twój wynik: {self.score}",True,(255,255,255))
            self.screen.blit(txt, (SCREEN_WIDTH//2-txt.get_width()//2, SCREEN_HEIGHT//2-60))
            self.screen.blit(fs, (SCREEN_WIDTH//2-fs.get_width()//2, SCREEN_HEIGHT//2))
            if pygame.time.get_ticks()-self.game_over_time>2000:
                rect = self.play_button.rect
                rect.top = SCREEN_HEIGHT//2+80
                self.play_button.draw(self.screen)
