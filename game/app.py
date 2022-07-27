import os
import pygame


class Component:

    def __init__(self, x, y, img_path):
        self.x = x
        self.y = y
        self.intended_x = x
        self.intended_y = y
        # self.img = pygame.image.load(os.path.join("assets", img_path))
        self.img = pygame.transform.scale(pygame.image.load(os.path.join("assets", img_path)), (32, 32))
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

    def __init__(self, x, y, img_path):
        super().__init__(x, y, img_path)

    def render(self):
        pass
# class Asteroid():


