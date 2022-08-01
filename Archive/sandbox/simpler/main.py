import pygame
import sys

from sprites import *
from settings import *


class Game:

    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font('COMIC.ttf', 16)

        self.intro_background = pygame.image.load('title_screen.jpg')

        self.running = True
        self.playing = False

    def create_tilemap(self):
        for y, row in enumerate(tilemap):
            for x, position in enumerate(row):
                if position == 'B':
                    Block(self, x, y)
                if position == 'P':
                    Player(self, x, y)
                if position == 'E':
                    Enemy(self, x, y)
                if position == 'U':
                    Upgrade(self, x, y)

    def run(self):
        """run game"""
        self.playing = True

        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.blocks = pygame.sprite.LayeredUpdates()
        self.upgrades = pygame.sprite.LayeredUpdates()
        self.enemies = pygame.sprite.LayeredUpdates()
        self.attacks = pygame.sprite.LayeredUpdates()

        self.create_tilemap()

    def events(self):
        """listens for events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False

    def update(self):
        self.all_sprites.update()

    def draw(self):
        self.screen.fill((0, 0, 0))
        self.all_sprites.draw(self.screen)
        self.clock.tick(FPS)

        pygame.display.update()

    def main(self):
        while self.playing:
            self.events()
            self.update()
            self.draw()
        self.running = False

    def intro(self):
        intro = True

        title = self.font.render('Crypto Astroneer', False, (255, 255, 255))
        title_rect = title.get_rect(x=10, y=10)

        play_button = Button(10, 50, 100, 50, (0, 0, 0), (255, 255, 255), 'PLAY', 16)

        while intro:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    intro = False
                    self.running = False

            mouse_position = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()  # returns list[int], left click is [0]

            if play_button.pressed(mouse_position, mouse_pressed):
                intro = False

            self.screen.blit(self.intro_background, (0, 0))
            self.screen.blit(title, title_rect)
            self.screen.blit(play_button.image, play_button.rect)

            self.clock.tick(FPS)
            pygame.display.update()

    # def game_over(self):
    #     text = self.font.render('GAME OVER', False, (255, 255, 255))
    #     text_rect = text.get_rect(center=(WIN_WIDTH/2, WIN_HEIGHT/2))
    #
    #     for sprite in self.all_sprites:
    #         sprite.kill()



if __name__ == '__main__':
    game = Game()
    game.intro()
    game.run()
    while game.running:
        game.main()
        # game.game_over()

    pygame.quit()

