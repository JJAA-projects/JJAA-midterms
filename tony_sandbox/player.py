import pygame


class Player:
    """player object"""

    def __init__(self, game):
        """initialize player object and its starting position"""
        self.screen = game.screen
        self.screen_rect = game.screen.get_rect()

        self.image = pygame.image.load('assets/file.bmp')
        self.rect = self.image.get_rect()

        # temporary, change this to something more appropriate later
        # self.rect.midbottom = self.screen_rect.midbottom

    def blitme(self):
        """renders the player object"""
        self.screen.blit(self.image, self.rect)

