import os
import pygame


class Component:

    def __init__(self, x, y, img_path, angle = 0):
        self.angle = 90
        self.x = x
        self.y = y
        self.intended_x = x
        self.intended_y = y
        # self.img = pygame.image.load(os.path.join("assets", img_path))
        self.img = pygame.transform.rotate(pygame.transform.scale(pygame.image.load(
            os.path.join("assets", img_path)), (32, 32)), self.angle)
        # self.facing = 0

    def move(self, direction):
        # self.x += distance
        # self.y += distance
        if direction == "left":
            self.intended_x -= 16
            # if self.facing != 3:
            #   load left facing sprite into self.image
            #   self.facing = 3
        if direction == "right":
            self.intended_x += 16
        if direction == "up":
            self.intended_y -= 16
        if direction == "down":
            self.intended_y += 16

    def update(self):
        if self.intended_x > self.x:
            self.x += 2
        if self.intended_x < self.x:
            self.x -= 2
        if self.intended_y > self.y:
            self.y += 2
        if self.intended_y < self.y:
            self.y -= 2

    # def tile_to_pixel(self, x, y):
    #     return (x*16, y*16)


class Ship(Component):
    def __init__(self, x, y, img_path, angle = 0):
        self.angle = 0
        self.x = x
        self.y = y
        self.intended_x = x
        self.intended_y = y
        # self.img = pygame.image.load(os.path.join("assets", img_path))
        self.img = pygame.transform.scale(pygame.image.load(
            os.path.join("assets", img_path)), (48, 48))
        # self.facing = 0
        self.mask = pygame.mask.from_surface(self.img)

    def collision(self, obj):
        return collide(self, obj)

    def rotate_img(self, angle):
        self.angle = angle

    def render(self):
        pass


class Asteroid(Component):
    def __init__(self, x, y, img_path):
        self.x = x
        self.y = y
        self.intended_x = x
        self.intended_y = y
        # self.img = pygame.image.load(os.path.join("assets", img_path))
        self.img = pygame.transform.scale(pygame.image.load(
            os.path.join("assets", img_path)), (96, 96))
        # self.facing = 0
        self.mask = pygame.mask.from_surface(self.img)


def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    if obj1.mask.overlap(obj2.mask, (offset_x,offset_y)) is not None:
        print("collided")
        return True
