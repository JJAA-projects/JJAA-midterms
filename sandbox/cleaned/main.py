import pygame
import sys

from sprites import *
from settings import *
from tiles import *

class Game:

    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Crypto Astroneer")
        self.screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.get_default_font()  # can be customized
        self.running = True
        self.playing = False
        # TODO: BOOL for titlescreen. Stop all playerfunction and don't render player while this is true. Set to
        #  false when player starts the game
        self.bg = pygame.image.load("assets/title_screen.jpg")
        self.bg = pygame.transform.scale(self.bg, (960, 640))

    def run(self):
        """run game"""
        self.playing = True

        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.tile_map = TileMap("sandbox/cleaned/Testmap02.csv", self.all_sprites)
        self.blocks = pygame.sprite.LayeredUpdates()
        self.enemies = pygame.sprite.LayeredUpdates()
        self.attacks = pygame.sprite.LayeredUpdates()

        self.player = Player(self, 1, 1)

    def events(self):
        """listens for events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False

    def update(self):
        self.all_sprites.update()

    def draw(self):
        # TODO: Change this to load the tilemap
        # self.screen.fill((0, 0, 0))
        # self.screen.blit(self.bg, (0, 0))
        self.tile_map.draw_map(self.screen)
        # self.screen.blit(self.tile_map.map_surface, (0, 0))
        self.all_sprites.draw(self.screen)
        self.clock.tick(FPS)
        pygame.display.update()

    def main(self):
        while self.playing:
            self.events()
            self.update()
            self.draw()
        self.running = False


if __name__ == '__main__':
    game = Game()
    game.run()
    while game.running:
        game.main()

    pygame.quit()

