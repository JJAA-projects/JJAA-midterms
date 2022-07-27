
import sys
import pygame

from settings import Settings
# from the settings.py module import the Settings class

from player import Player
# from the player.py module import the Player class


class Game:
    """Game logic"""

    def __init__(self):
        """Initializes game and creates resources"""
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Window Title")

        self.player = Player(self)

    def _check_events(self):
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

    def _update_screen(self):
        """helper method that updates screen"""
        self.screen.fill(self.settings.bg_color)  # redraws BG each pass through loop
        self.player.blitme()
        pygame.display.flip()  # updates screen

    def run_game(self):
        """Main game loop"""

        while True:
            self._check_events()  # checks for keyboard and mouse events
            self._update_screen()  # update images and flip to new screens


if __name__ == '__main__':

    game = Game()  # create instance
    game.run_game()  # run game
