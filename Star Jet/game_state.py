# game_state.py
# ——————————————————————————————
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
        self.background = pygame.image.load(os.path.join("assets","images","background.png")).convert()
        self.explosion_sound = pygame.mixer.Sound(os.path.join("assets","sounds","explosion.wav"))

        r = pygame.Rect((SCREEN_WIDTH-200)//2,(SCREEN_HEIGHT-60)//2,200,60)
        self.play_button = Button("GRAJ", r, self.font)
        self.scoreboard = Scoreboard(self.font,(10,10))

        self.reset_game()
        self.game_active = False
        self.game_over = False
        self.game_over_time = 0

        # bonusy
        self.bonus_group = pygame.sprite.Group()
        self.bonus_timer = 0

    def reset_game(self):
        self.player      = Player()
        self.enemy_group = pygame.sprite.Group(Enemy() for _ in range(5))
        self.effects     = pygame.sprite.Group()
        self.score       = 0
        self.milestones  = [10,20,40,60,100]
        self.added       = [5,10,15,20,25]
        self.idx         = 0
        self.spawn_t     = 0
        self.game_over   = False
        self.player.health = self.player.max_health
        for e in self.enemy_group: e.health = e.max_health

    def handle_event(self,event):
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
        if not self.game_active or self.game_over: return

        keys = pygame.key.get_pressed()
        self.player.update(keys)
        self.enemy_group.update()
        self.effects.update()
        self.bonus_group.update()

        # pociski ↔ wrogowie
        hits = pygame.sprite.groupcollide(self.player.bullets, self.enemy_group, True, False)
        for bullet, enemies in hits.items():
            for enemy in enemies:
                enemy.health -=1
                if enemy.health<=0:
                    self.effects.add(Explosion(enemy.rect.centerx,enemy.rect.centery))
                    self.explosion_sound.play()
                    enemy.kill()
                    self.score+=1

        # bonusy ↔ gracz
        coups = pygame.sprite.spritecollide(self.player, self.bonus_group, True)
        for b in coups:
            if b.kind=='health':
                self.player.health = min(self.player.max_health, self.player.health+1)
            elif b.kind=='homing':
                self.player.homing = True
                self.player.homing_ticks = FPS*5  # 5 sekund homingu

        # progi
        if self.idx<len(self.milestones) and self.score>=self.milestones[self.idx]:
            for _ in range(self.added[self.idx]):
                self.enemy_group.add(Enemy())
            self.idx+=1

        # gracz ↔ wróg
        if pygame.sprite.spritecollideany(self.player, self.enemy_group):
            self.game_over = True
            self.game_over_time = pygame.time.get_ticks()

        # okresowy spawn wroga
        self.spawn_t+=1
        if self.spawn_t>=FPS*2:
            self.enemy_group.add(Enemy())
            self.spawn_t=0

        # bonus spawn
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
