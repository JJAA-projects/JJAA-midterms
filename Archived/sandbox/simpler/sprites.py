import pygame
from settings import *
import math
import random


class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.currency = 1000
        self.power = 0

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.x_change = 0
        self.y_change = 0

        self.facing = 'down'
        self.animation_loop = 1

        self.image = pygame.Surface([self.width, self.height])  # can be used as placeholder
        self.image.fill((255, 255, 0))  # fills rectangle with RGB color
        # self.image = pygame.image.load('assets/player_front.png', 'Miner49er')

        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.x, self.y

    def update(self):
        self.movement()
        self.collide_death()
        # self.animate()

        self.rect.x += self.x_change
        self.collide('x')
        self.rect.y += self.y_change
        self.collide('y')

        self.x_change = 0
        self.y_change = 0

    def movement(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            for sprite in self.game.all_sprites:
                sprite.rect.x += PLAYER_SPEED
            self.x_change -= PLAYER_SPEED
            self.facing = 'left'
        if keys[pygame.K_RIGHT]:
            for sprite in self.game.all_sprites:
                sprite.rect.x -= PLAYER_SPEED
            self.x_change += PLAYER_SPEED
            self.facing = 'right'
        if keys[pygame.K_UP]:
            for sprite in self.game.all_sprites:
                sprite.rect.y += PLAYER_SPEED
            self.y_change -= PLAYER_SPEED
            self.facing = 'up'
        if keys[pygame.K_DOWN]:
            for sprite in self.game.all_sprites:
                sprite.rect.y -= PLAYER_SPEED
            self.y_change += PLAYER_SPEED
            self.facing = 'down'

    # def upgrade(self):
    #
    #     hits = pygame.sprite.spritecollide(self, self.game.upgrades, False)
    #     # TODO: write logic so after collision check, check currency and subtract to upgrade player object
    #
    #     if hits:
    #         if self.currency >= 1000:
    #             self.power += 1
    #             # TODO: update power text on screen
    #         else:
    #             pass

    def collide(self, direction):

        # checks if sprite rects overlap, Boolean to delete collided sprite
        hits = pygame.sprite.spritecollide(self, self.game.blocks, False)

        if direction == 'x':
            if hits:  # subtracts length of collided object, effectively keeping player in place
                if self.x_change > 0:
                    self.rect.x = hits[0].rect.left - self.rect.width
                    for sprite in self.game.all_sprites:
                        sprite.rect.x += PLAYER_SPEED  # counters screen scrolling against collision
                if self.x_change < 0:
                    self.rect.x = hits[0].rect.right
                    for sprite in self.game.all_sprites:
                        sprite.rect.x -= PLAYER_SPEED

        if direction == 'y':
            if hits:
                if self.y_change > 0:
                    self.rect.y = hits[0].rect.top - self.rect.height
                    for sprite in self.game.all_sprites:
                        sprite.rect.y += PLAYER_SPEED
                if self.y_change < 0:
                    self.rect.y = hits[0].rect.bottom
                    for sprite in self.game.all_sprites:
                        sprite.rect.y -= PLAYER_SPEED

    def collide_death(self):
        hits = pygame.sprite.spritecollide(self, self.game.enemies, False)
        if hits:
            self.kill()
            self.game.playing = False


    # def animate(self):
    #     attack_animations = [self.image0, self.image1, self.image2]
    #
    #     if self.facing == 'attack':
    #         if self.attack == True:
    #             self.image = attack_animations[math.floor(self.animation_loop)]
    #             self.animation_loop += 0.1  # sums to 10 every 10 FPS
    #             if self.animation_loop >= 3:  # ^ so swaps sprite every 10 frames between index 1 and 2
    #                 self.animation_loop = 1  # resets back to index 1, index 0 is standing sprite
    #         else:
    #             self.image = self.facingimage

class Enemy(pygame.sprite.Sprite):

    def __init__(self, game, x, y):

        self.game = game
        self._layer = ENEMY_LAYER
        self.groups = self.game.all_sprites, self.game.enemies
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.x_change = 0
        self.y_change = 0

        self.image = pygame.Surface([self.width, self.height])  # can be used as placeholder
        self.image.fill((255, 0, 255))  # fills rectangle with RGB color

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self):
        self.rect.x += self.x_change
        self.rect.y += self.y_change

        self.x_change = 0
        self.y_change = 0


class Upgrade(pygame.sprite.Sprite):

    def __init__(self, game, x, y):

        self.game = game
        self._layer = UPGRADE_LAYER
        self.groups = self.game.all_sprites, self.game.upgrades
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = pygame.Surface([self.width, self.height])  # creates the surface size for image to occupy
        self.image.fill((0, 0, 255))

        self.rect = self.image.get_rect()  # creates the underlying rectangle used for detection and position
        self.rect.x = self.x
        self.rect.y = self.y


class Block(pygame.sprite.Sprite):

    def __init__(self, game, x, y):

        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites, self.game.blocks  # assigns to all sprites and block groups
        pygame.sprite.Sprite.__init__(self, self.groups)  # allows Block class to be added to inherited groups

        # sets coordinates and dimensions of surface
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = pygame.Surface([self.width, self.height])  # creates the surface size for image to occupy
        self.image.fill((255, 0, 0))

        self.rect = self.image.get_rect()  # creates the underlying rectangle used for detection and position
        self.rect.x = self.x
        self.rect.y = self.y


class Button:
    def __init__(self, x, y, width, height, fg, bg, content, size):
        self.font = pygame.font.Font('COMIC.ttf', size)
        self.content = content

        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.fg = fg
        self.bg = bg

        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(self.bg)
        self.rect = self.image.get_rect()

        self.rect.x = self.x
        self.rect.y = self.y

        self.text = self.font.render(self.content, False, self.fg)  # text, anti aliasing, color
        self.text_rect = self.text.get_rect(center=(self.width/2, self.height/2))  # centers text on button
        self.image.blit(self.text, self.text_rect)  # blits text onto image

    def pressed(self, position, pressed):
        if self.rect.collidepoint(position):
            if pressed[0]:
                return True
            return False
        return False


