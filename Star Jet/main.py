import pygame
from settings import *
from player import Player
from enemy import Enemy
import random

pygame.init()
icon = pygame.image.load("assets/icon.png")
pygame.display.set_icon(icon)




screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Star Jet")
clock = pygame.time.Clock()

background = pygame.image.load("assets/background.png")
font = pygame.font.SysFont(None, 36)
game_active = False
game_over = False
game_over_time = None

score = 0
milestones = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
added_enemies = [5, 10, 15, 20, 25, 30, 35, 40, 45, 50]
milestone_index = 0
spawn_timer = 0

player = Player()
enemy_group = pygame.sprite.Group([Enemy() for _ in range(5)])

# Parametry przycisku PLAY
button_width, button_height = 200, 60
button_rect = pygame.Rect(
    (SCREEN_WIDTH - button_width) // 2,
    (SCREEN_HEIGHT - button_height) // 2,
    button_width,
    button_height
)
button_color = (0, 200, 0)
hover_color = (0, 255, 0)
text_color = (0, 0, 0)

def draw_play_button(surface, rect, font):
    mouse_pos = pygame.mouse.get_pos()
    color = hover_color if rect.collidepoint(mouse_pos) else button_color
    pygame.draw.rect(surface, color, rect)
    label = font.render("PLAY", True, text_color)
    label_rect = label.get_rect(center=rect.center)
    surface.blit(label, label_rect)

def reset_game():
    global player, enemy_group, score, milestone_index, game_over, spawn_timer, game_over_time
    player = Player()
    enemy_group = pygame.sprite.Group([Enemy() for _ in range(5)])
    score = 0
    milestone_index = 0
    game_over = False
    spawn_timer = 0
    game_over_time = None

running = True
while running:
    clock.tick(FPS)
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if not game_active:
        draw_play_button(screen, button_rect, font)
        if pygame.mouse.get_pressed()[0] and button_rect.collidepoint(pygame.mouse.get_pos()):
            game_active = True
            reset_game()

    elif not game_over:
        keys = pygame.key.get_pressed()
        player.update(keys)
        player.draw(screen)

        enemy_group.update()
        enemy_group.draw(screen)

        # Kolizja pocisków z wrogami + punktacja
        hits = pygame.sprite.groupcollide(player.bullets, enemy_group, True, True)
        score += len(hits)

        # Dodawanie wrogów przy osiągnięciu progu
        if milestone_index < len(milestones) and score >= milestones[milestone_index]:
            count = added_enemies[milestone_index]
            for _ in range(count):
                enemy_group.add(Enemy())
            milestone_index += 1

        # Kolizja gracza z wrogiem
        for enemy in enemy_group:
            if enemy.rect.colliderect(player.rect):
                game_over = True
                game_over_time = pygame.time.get_ticks()
                break

        # (opcjonalne) Dodawanie wrogów co jakiś czas
        spawn_timer += 1
        if spawn_timer >= 120:
            enemy_group.add(Enemy())
            spawn_timer = 0

        # Wyświetlanie punktów
        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))

    else:
        text = font.render("GAME OVER", True, (255, 0, 0))
        final_score = font.render(f"Final Score: {score}", True, (255, 255, 255))
        screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2,
                           SCREEN_HEIGHT // 2 - 60))
        screen.blit(final_score, (SCREEN_WIDTH // 2 - final_score.get_width() // 2,
                                  SCREEN_HEIGHT // 2))

        if game_over_time and pygame.time.get_ticks() - game_over_time > 2000:
            # Ustaw nową pozycję przycisku na dole
            play_rect = button_rect.copy()
            play_rect.top = SCREEN_HEIGHT // 2 + 80
            draw_play_button(screen, play_rect, font)

            if pygame.mouse.get_pressed()[0] and play_rect.collidepoint(pygame.mouse.get_pos()):
                game_active = True
                reset_game()


    pygame.display.flip()

pygame.quit()
