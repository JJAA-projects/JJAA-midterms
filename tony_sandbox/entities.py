import pygame


class Edge(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        # will need layers and groups later for collisions
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * 16
        self.y = y * 16
        self.width = 16
        self.height = 16

        self.image = pygame.image.load('MapAsteroidTopLeft.png')
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.x, self.y

