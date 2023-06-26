import random
import time

import pygame
import pathlib
import Objects
from pygame import mixer

#Initialize Pygame
pygame.init()

#Functions
def init_icon():
    enemy_icon = str(pathlib.Path.cwd()).replace("\\", "/").replace("Scripts", "Assets")
    enemy_icon = pathlib.Path(enemy_icon) / "yellow.png"
    return enemy_icon


def init_bg():
    bg = str(pathlib.Path.cwd()).replace("\\", "/").replace("Scripts", "Assets")
    bg = pathlib.Path(bg) / "Space-Invaders-BG.jpg"
    return bg


def ambient_music():
    route  = str(pathlib.Path.cwd() / "MusicaFondo.mp3").replace("\\", "/").replace("Scripts", "Assets")
    mixer.music.load(route)
    mixer.music.set_volume(.4)
    mixer.music.play(-1)

#Creates the screen
screen = pygame.display.set_mode((1600, 900))

#Screen set-up
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load(init_icon())
pygame.display.set_icon(icon)
bg = pygame.image.load(init_bg())

#Objects
score = Objects.Score(screen)
player = Objects.Player(screen, score)
enemies = []
for i in range(20):
    enemies.append(Objects.Enemy(random.randint(30, 1538), random.randint(0, 300), screen, random.randint(-1,0)))

bullets = player.get_bullets()

#Music
ambient_music()

#Game loop
exit = False
in_game = True

while not exit:
    screen.blit(bg, (0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                player.move_input("a")
            elif event.key == pygame.K_d:
                player.move_input("d")

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                player.stop("a")
            elif event.key == pygame.K_d:
                player.stop("d")
            if event.key == pygame.K_SPACE:
                player.shoot()

    player.move_player()

    for enemy in enemies:
        in_game = enemy.move_enemy()

        if not in_game:
            for e in enemies:
                e.game_over()
            for b in bullets:
                b.game_over()
            break

        for bullet in bullets:
            bullet.move()
            bullet.detect_collision(enemy)

    if in_game:
        score.update_score()
        pygame.display.update()
    else:
        score.game_over_text()
        pygame.display.update()
        time.sleep(3)
        break