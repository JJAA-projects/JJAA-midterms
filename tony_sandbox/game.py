
import sys
import pygame

from settings import Settings
# from the settings.py module import the Settings class

from player import Player
# from the player.py module import the Player

from tiles import *


class Game:
    """Game logic"""

    def __init__(self):
        """Initializes game and creates resources"""
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        self.canvas = pygame.Surface((self.settings.screen_width, self.settings.screen_height))

        pygame.display.set_caption("Window Title")

        self.player = Player(self)
        self.zone = TileMap('test_level.csv')

        # self.player_rect.x, self.player_rect.y = self.zone.start_x, self.zone.start_y

    def check_events(self):
        """helper method that checks for exit commands"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    self.player.rect.x += 16
                if event.key == pygame.K_LEFT:
                    self.player.rect.x -= 16
                if event.key == pygame.K_UP:
                    self.player.rect.y -= 16
                if event.key == pygame.K_DOWN:
                    self.player.rect.y += 16

    def update_screen(self):
        """helper method that updates screen"""
        self.screen.fill(self.settings.bg_color)  # redraws BG each pass through loop
        self.player.blitme()
        pygame.display.flip()  # updates screen
        # self.canvas.fill((0, 0, 0))
        # self.zone.draw_map(self.canvas)

    def create_tilemap(self):
        for y, row in enumerate(tilemap):
            for x, column in enumerate(row):
                if column == 'E':
                    Edge(self, x, y)
                if column == '0':
                    Player(self, x, y)



    def run_game(self):
        """Main game loop"""

        while True:

            self.check_events()  # checks for keyboard and mouse events
            self.update_screen()  # update images and flip to new screens


if __name__ == '__main__':

    game = Game()  # create instance
    game.run_game()  # run game
