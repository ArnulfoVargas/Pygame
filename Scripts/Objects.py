import pathlib
import random
import pygame
import time
import math
from pygame import mixer

class Player:
    _x_position = 0
    _y_position = 0
    _player = ""
    _screen = 0
    _speed = 0
    _key = ''
    _bullets = []
    _i = 0
    _last_shoot = 0
    _sound = ""

    def __init__(self, screen, score):
        self._player = pathlib.Path(str(pathlib.Path.cwd()).replace("\\", "/").replace("Scripts", "Assets")) / "player.png"
        self._sound = mixer.Sound(pathlib.Path(str(pathlib.Path.cwd()).replace("\\", "/").replace("Scripts", "Assets")) / "disparo.mp3")
        self._x_position = 770
        self._y_position = 870
        self._speed = 0
        self._key = " "
        self._screen = screen
        self._last_shoot = -1

        self._i = 0

        for i in range(10):
            self._bullets.append(Bullet(0, screen, False, score))

        self._player = pygame.image.load(self._player)


    def _draw_player(self):
        self._screen.blit(self._player, (self._x_position, self._y_position))


    def move_player(self):
        self._x_position += self._speed

        if self._x_position > 1540:
            self._x_position = 1540
        elif self._x_position < 0:
            self._x_position = 0

        self._draw_player()


    def move_input(self, key):
        if key == "a" and key != self._key:
            self._speed = -.65
        elif key == "d" and key != self._key:
            self._speed = .65

        self._key = key


    def stop(self, key):
        if self._key == key:
            self._key = " "
            self._speed = 0


    def shoot(self):
        if (time.time() - self._last_shoot) > .25:
            self._bullets[self._i].shoot(self._x_position + 26)
            self._sound.play()
            self._i = (self._i + 1) % 10
            self._last_shoot = time.time()

    def get_bullets(self):
        return self._bullets


class Enemy:
    _x_position = 0
    _y_position = 0
    _speed = 0
    _enemy = ""
    _out = False
    _screen = 0

    def __init__(self, x_position, y_position, screen, direction):
        self._x_position = x_position - 16
        self._y_position = y_position
        self._speed = .5 + direction
        self._out = False
        self._screen = screen
        self._enemy = pathlib.Path(str(pathlib.Path.cwd()).replace("\\", "/").replace("Scripts", "Assets")) / "yellow.png"
        self._enemy = pygame.image.load(self._enemy)


    def _draw_enemy(self):
        self._screen.blit(self._enemy, (self._x_position, self._y_position))


    def move_enemy(self):
        if (self._x_position > 1568 or self._x_position < 0) and not self._out:
            self._speed = self._speed * -1.25
            self._y_position += 50

            if self._y_position > 600:
                return False

            self._out = True

        else:
            self._out = False

        self._x_position += self._speed
        self._draw_enemy()
        return True

    def game_over(self):
        self._y_position = -1000
        self._x_position = 200
        self._speed = 0
        self._draw_enemy()

    def get_position(self):
        return self._x_position, self._y_position


    def respawn(self):
        self._x_position = random.randint(0, 1568)
        self._y_position = random.randint(5, 300)
        self._speed = .5


class Bullet:
    _bullet = ""
    _x_position = 0
    _y_position = 0
    _speed = 0
    _screen = 0
    _visibility = False
    _score = 0
    _death = 0

    def __init__(self, _x_position, screen, visibility, score):
        self._bullet = pathlib.Path(str(pathlib.Path.cwd()).replace("\\", "/").replace("Scripts", "Assets")) / "extra.png"
        self._bullet = pygame.image.load(self._bullet)
        self._death = mixer.Sound(pathlib.Path(str(pathlib.Path.cwd()).replace("\\", "/").replace("Scripts", "Assets")) / "Golpe.mp3")
        self._x_position = _x_position
        self._y_position = 840
        self._speed = .1
        self._screen = screen
        self._score = score

    def shoot(self, x_pos):
        self._y_position = 840
        self._visibility = True
        self._x_position = x_pos


    def detect_collision(self, enemy):
        global counter
        b_x_pos, b_y_pos = enemy.get_position()
        distance = math.sqrt(((self._x_position - b_x_pos)**2 + (self._y_position - b_y_pos)**2))

        if distance < 30 and self._visibility:
            self._death.play()
            self._visibility = False
            self._score.add_score()

            enemy.respawn()


    def move(self):
        if self._visibility:
            self._y_position -= self._speed
            self._screen.blit(self._bullet, (self._x_position, self._y_position))

            if self._y_position < 0:
                self._visibility = False

    def game_over(self):
        self._visibility = False
        self._y_position = -100
        self._speed = 0
        self._screen.blit(self._bullet, (self._x_position, self._y_position))


class Score:
    _font = ""
    _txt_x = 0
    _txt_y = 0
    _score = 0
    _screen = 0

    def __init__(self, screen):
        self._font = pygame.font.Font("freesansbold.ttf", 32)
        self._txt_y = 10
        self._txt_x = 10
        self._score = 0
        self._screen = screen


    def update_score(self):
        txt = self._font.render(f"Score: {self._score}", True, (255,255,255))
        self._screen.blit(txt, (self._txt_x, self._txt_y))


    def add_score(self):
        self._score += 1

    def game_over_text(self):
        self._font = pygame.font.Font("freesansbold.ttf", 200)
        txt = self._font.render(f"GAME OVER", True, (255, 255, 255))
        self._screen.blit(txt, (200, 400))

