from turtle import window_height, window_width
import pygame
import math
import random
import typing

try:
    from settings import *
except e:
    from game.settings import *


class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y, group, collision_map):
        self.game = game
        self.is_game_over: bool = False
        self._layer = PLAYER_LAYER
        self.groups = group
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x: int = x * WIN_WIDTH / 2 - TILESIZE
        self.y: int = y * WIN_HEIGHT / 2
        self.width = TILESIZE * 1.5
        self.height = TILESIZE * 1.5

        self.collision_map = collision_map

        self.x_change: int = 0
        self.y_change: int = 0

        self.player_is_ship: bool = True
        self.facing: str = 'up'
        self.action_timer: int = 0
        self.action_timer_max = ACTION_TIMER
        self.miner_image_set = {
            'left': pygame.transform.scale(pygame.image.load('assets/Miner/MinerLeftStand.bmp', 'Miner49er'),
                                           (TILESIZE, TILESIZE)),
            'right': pygame.transform.scale(pygame.image.load('assets/Miner/MinerRightStand.bmp', 'Miner49er'),
                                           (TILESIZE, TILESIZE)),
            'up': pygame.transform.scale(pygame.image.load('assets/Miner/MinerUpStand.bmp', 'Miner49er'),
                                           (TILESIZE, TILESIZE)),
            'down': pygame.transform.scale(pygame.image.load('assets/Miner/MinerDownStand.bmp', 'Miner49er'),
                                           (TILESIZE, TILESIZE))
        }
        self.ship_image = pygame.transform.scale(pygame.image.load('assets/Ship/ShipUpFlying.bmp', 'Ship'),
                                           (TILESIZE, TILESIZE))
        self.ship_image_set = {
            'left': pygame.transform.rotate(self.ship_image, 90),
            'right': pygame.transform.rotate(self.ship_image, 270),
            'up': self.ship_image,
            'down': pygame.transform.rotate(self.ship_image, 180)
        }

        self.image = self.miner_image_set['down']
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.x, self.y
        self.last_pos_x, self.last_pos_y = 0, 0
        self.mask = pygame.mask.from_surface(self.image)

    def update(self) -> None:
        if self.action_timer > 7:
            if self.movement():
                self.action_timer = 0
        else:
            self.action_timer += 1

        if not self.player_is_ship:
            self.image = self.miner_image_set[self.facing]
        else:
            self.image = self.ship_image_set[self.facing]

        self.rect.x += self.x_change
        self.rect.y += self.y_change

        self.x_change = 0
        self.y_change = 0

    def movement(self) -> None:
        keys = pygame.key.get_pressed()
        if not self.is_game_over:
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                if (self.rect.x/TILESIZE) -1 >= 0 and self.collision_map[int(self.rect.y / TILESIZE)][int(self.rect.x / TILESIZE) - 1] == 0:
                    self.x_change -= TILESIZE
                    self.facing = 'left'
                    return True
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                if (self.rect.x/TILESIZE) +1 <= 29 and self.collision_map[int(self.rect.y / TILESIZE)][int(self.rect.x / TILESIZE) + 1] == 0:
                    self.x_change += TILESIZE
                    self.facing = 'right'
                    return True
            if keys[pygame.K_UP] or keys[pygame.K_w]:
                if (self.rect.y/TILESIZE) -1 >= 0 and self.collision_map[int(self.rect.y / TILESIZE) - 1][int(self.rect.x / TILESIZE)] == 0:
                    self.y_change -= TILESIZE
                    self.facing = 'up'
                    return True
            if keys[pygame.K_DOWN] or keys[pygame.K_s]:
                if (self.rect.y/TILESIZE) + 1 <= 19 and self.collision_map[int(self.rect.y / TILESIZE) + 1][int(self.rect.x / TILESIZE)] == 0:
                    self.y_change += TILESIZE
                    self.facing = 'down'
                    return True
